''' vault_man.py

Vault Man represents an in memory vault.
- It can be saved to disk as encrypted r3dv1t arkive. 
- It can dump its contents to a specified folder
.... 


'''

import os
import sys
import io
import json
import hashlib
import hmac
import gc

import base64 as b64

from nacl.secret import SecretBox

from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t.errors import R3D_IO_Error, R3D_V1T_Error
from libr3dv1t.typedefs import MemObj, CTSegment, RVKryptMode
from libr3dv1t.krypt_utilz import kdf
from libr3dv1t.utilz.vvfs import VVFS
from libr3dv1t.krypt_utilz.nonce_gen import make_nonce
from libr3dv1t.log_utilz.log_man import current_logger as log


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class VaultMan:
    """ An in memory r3d vault. """

    # --------------------------------------------------------------------------------------------------------------------------
    def __init__(self, vlt_file_pathname_to_load: str = None, krypt_mode: RVKryptMode = RVKryptMode.CHACHA20_POLY1305):

        self._krypt_mode = krypt_mode

        if vlt_file_pathname_to_load is None:
            self.init_new_arkive()
            log.info("Initialized a new arkive.")
        else:
            self.init_from_file_pathname(vlt_file_pathname_to_load)

        self.vks = kdf.vks_set_from_user_pass(b"change_me")
        log.info(f"self.vks: {self.vks}")

    # --------------------------------------------------------------------------------------------------------------------------
    def init_new_arkive(self):

        # map from oid -> mem_obj
        # memory object store
        self.mem_os = {}

        # vault virtual file system
        self.vvfs = VVFS()

    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------- read vault
    def init_from_file_pathname(self, vlt_file_pathname: str):
        """ Initialize the vault manager from an existing vault file. """

        self.mem_os = {}
        if not os.path.exists(vlt_file_pathname):
            raise R3D_IO_Error(f"Vault file {vlt_file_pathname} does not exist.")

        # --- read the vault file and process each frame line
        with open(vlt_file_pathname, "rb") as fh:
            for line in fh:
                try:
                    self.process_frame_line(line)
                except Exception as e:
                    log.warn(e)
                    continue

        # --- decrypt all segments, construct vault objects in memory
        for mem_obj in self.vibk.values():
            try:
                self.decrypt_mem_obj(mem_obj)
            except Exception as e:
                log.warn(e)
                continue

    # --------------------------------------------------------------------------------------------------------------------------
    def process_frame_line(self, line: bytes):
        """ Process a single frame line from the vault file and update in mem structures accordingly . """

        fields = line.strip().split(b'|')
        if len(fields) != 3:
            raise R3D_V1T_Error(f"Invalid frame line @ line starting with: {line[:10]}")

        lfp = fields[0]  # line fingerprint
        meta_dict_b64 = fields[1]  # base64 encoded metadata dict
        ct_chunk_b64 = fields[2]  # ciphertext chunk

        # --- validate lfp, continue if failed
        lfp_check = hashlib.sha3_256(meta_dict_b64 + ct_chunk_b64).hexdigest().encode("ascii")
        if lfp != lfp_check:
            raise R3D_V1T_Error(f"Invalid frame: LFP fail @ line starting with: {line[:10]}")

        # --- decode meta dict
        meta_dict = {}
        try:
            meta_dict = json.loads(b64.urlsafe_b64decode(meta_dict_b64).decode("utf-8"))
        except Exception as e:
            raise R3D_V1T_Error(f"Invalid frame: meta_dict does not decode @ Line starting with: {lfp[:10]}")

        # --- create segment object
        ct_seg = CTSegment()
        ct_seg.idx = meta_dict['i']
        ct_seg.parent_obj_id = meta_dict['o']

        if RVKryptMode.CHACHA20_POLY1305.value in meta_dict:
            ct_seg.km = RVKryptMode.CHACHA20_POLY1305
            ct_seg.km_data = meta_dict[RVKryptMode.CHACHA20_POLY1305.value]
        elif RVKryptMode.FERNET.value in meta_dict:
            ct_seg.km = RVKryptMode.FERNET
            ct_seg.km_data = meta_dict[RVKryptMode.FERNET.value]
        else:
            raise R3D_V1T_Error(f"Invalid frame: unknown krypt mode @ Line starting with: {lfp[:10]}")

        # --- decode but not decrypt ct_chunk
        ct_seg.ct_chunk = b64.urlsafe_b64decode(ct_chunk_b64)

        # --- create or update vault object
        if ct_seg.parent_obj_id not in self.vibk:
            mem_obj = MemObj()
            mem_obj.obj_id = ct_seg.parent_obj_id
            mem_obj.ct_segments = [ct_seg]
            self.vibk[mem_obj.obj_id] = mem_obj
        else:
            mem_obj = self.vibk[ct_seg.parent_obj_id]
            mem_obj.ct_segments.append(ct_seg)

    # --------------------------------------------------------------------------------------------------------------------------
    def decrypt_mem_obj(self, mem_obj: MemObj):
        """ Decrypt a mem_obj using the vault keys and update in memory structures (pt_data). """

        if mem_obj.ct_segments is None:
            raise R3D_IO_Error("mem_obj has no ciphertext segments to decrypt.")

        # --- construct the full file in memory
        temp_fh = io.BytesIO()

        for ct_seg in mem_obj.ct_segments:
            if ct_seg.km == RVKryptMode.CHACHA20_POLY1305:
                # --- decrypt this chunk using the vault key
                # box = SecretBox(self.vks.sgk_chacha20_poly1305)
                # decrypted = box.decrypt(ct_seg.ct_chunk)
                # temp_fh.write(decrypted)
                temp_fh.seek(ct_seg.idx)
                temp_fh.write(ct_seg.ct_chunk)
            else:
                raise R3D_V1T_Error(f"Error decrypting segment: Unknown krypt mode in segment: {ct_seg}")

        mem_obj.pt_data = temp_fh.getvalue()
        temp_fh.close()
        gc.collect()

        # dont clear the ct_segments, they are needed for saving the vault later

    # --------------------------------------------------------------------------------------------------------------------------
    def xtract_vlt_to_path(self, xtraction_path: str):
        """ Extract the vault contents to the specified path. """

        if not os.path.exists(xtraction_path):
            os.makedirs(xtraction_path)

        for mem_obj in self.vibk.values():
            if mem_obj.pt_data is None:
                log.info(f"Vault object {mem_obj.obj_id} has no plaintext data to xtract.")
                continue

            try:
                output_file_path = os.path.join(xtraction_path, mem_obj.obj_id)
                with open(output_file_path, "wb") as fh:
                    fh.write(mem_obj.pt_data)
                    fh.flush()
            except Exception as e:
                log.warn(f"Error extracting vault object {mem_obj.obj_id}: {e}")
                continue

        # ---
        gc.collect()

    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------- save vault
    def put_object(self, pt_data: bytes, vopn: str):
        """ Upsert object into the vault. """

        # --- check if pt_data is bytes
        if not isinstance(pt_data, bytes):
            raise R3D_V1T_Error("put_object: pt_data must be a bytes instance.")

        # --- check if vopn is a valid path name
        if not isinstance(vopn, str):
            raise R3D_V1T_Error("put_object: vopn must be a string.")

        log.dbg(f"put_object: pt_data[:4]={pt_data[:4]} -- len(pt_data)={len(pt_data)} -- vopn='{vopn}'")

        mobj = MemObj()
        mobj.pt_data = pt_data

        # --- compute obj id
        # its the hmac_sha3_384 of pt_data using the key in self.vks.osfp_key
        mobj.obj_id = hmac.new(self.vks.osfp_key, pt_data, hashlib.sha3_384).hexdigest()

        self.mem_os[mobj.obj_id] = mobj
        self.encrypt_mem_obj(mobj)

        # --- update the vopn map
        self.vopn_map.upsert_vopn(vopn, mobj.obj_id)

    # --------------------------------------------------------------------------------------------------------------------------
    def encrypt_mem_obj(self, mem_obj: MemObj):
        """ Encrypt the vault object using the vault key. """

        if mem_obj.pt_data is None:
            raise R3D_IO_Error("Vault object has no plaintext data to encrypt.")

        chunk_size = _rvcc.default_chunk_size

        for i in range(0, len(mem_obj.pt_data), chunk_size):
            pt_chunk = mem_obj.pt_data[i:i + chunk_size]

            ct_seg = CTSegment()
            ct_seg.idx = i
            ct_seg.ct_chunk = b64.urlsafe_b64encode(pt_chunk)  # TODO encrypt this chunk using the vault key
            ct_seg.parent_obj_id = mem_obj.obj_id
            ct_seg.km = self._krypt_mode
            if ct_seg.km == RVKryptMode.CHACHA20_POLY1305:
                ct_seg.km_data = {}  # TODO
            elif ct_seg.km == RVKryptMode.FERNET:
                # ct_seg.km_data = {}
                raise NotImplementedError("Fernet encryption is not implemented yet.")
            else:
                raise R3D_V1T_Error(f"Unknown krypt mode: {ct_seg.km}")

            mem_obj.ct_segments.append(ct_seg)

    # --------------------------------------------------------------------------------------------------------------------------
    def save_vault(self, output_pathname: str):
        """ Save this vault to the output file. """

        with open(output_pathname, "wb") as fh:
            for mem_obj in self.vibk.values():
                for ct_seg in mem_obj.ct_segments:
                    meta_dict = {
                        "i": ct_seg.idx,  # starting offset of the chunk in the original file
                        "o": ct_seg.parent_obj_id,
                        ct_seg.km.value: ct_seg.km_data,
                    }

                    # encode meta dict
                    meta_dict_json_bytes = json.dumps(meta_dict).encode("ascii")
                    meta_dict_b64 = b64.urlsafe_b64encode(meta_dict_json_bytes)

                    # create line fingerprint
                    lfp = hashlib.sha3_256(meta_dict_b64 + ct_seg.ct_chunk).hexdigest().encode("ascii")

                    # [lfp] | [meta_dict_b64] | [chunk or frame payload]
                    line = lfp + b'|' + meta_dict_b64 + b'|' + ct_seg.ct_chunk + b'\n'
                    fh.write(line)
                    fh.write(line)  # TODO deal with replication

                # --- next mem_obj
                fh.write(b'\n\n\n')  # save a couple of invalid frame lines for debugging purposes
                fh.flush()

        # ---


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
