import os
import sys
import io
import json
import hashlib
import gc

import base64 as b64

from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t.errors import R3D_IO_Error
from libr3dv1t.typedefs import VaultObj, CTSegment
from libr3dv1t.krypt_utilz import kdf

'''


'''


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class VaultMan:
    """ Vault manager for the r3dv1t file format.
    This class is responsible for creating, reading, updating r3d v1t arkives.
    """

    # --------------------------------------------------------------------------------------------------------------------------
    def __init__(self, vlt_file_pathname_to_load: str = None):

        self._vlt_file_pathname_to_load = vlt_file_pathname_to_load

        if self._vlt_file_pathname_to_load is None:
            self.init_new_arkive()
            print("Initialized a new arkive.")
        else:
            self.init_from_file()

        self.vks = kdf.vks_set_from_user_pass(b"change_me")
        print(f"self.vks: {self.vks}")

    # --------------------------------------------------------------------------------------------------------------------------
    def init_from_file(self):
        """ Initialize the vault manager from an existing vault file. """

        self.vibk = {}
        if not os.path.exists(self._vlt_file_pathname_to_load):
            raise R3D_IO_Error(f"Vault file {self._vlt_file_pathname_to_load} does not exist.")

        with open(self._vlt_file_pathname_to_load, "rb") as fh:
            for line in fh:
                fields = line.strip().split(b'|')
                if len(fields) != 3:
                    continue
                lfp = fields[0]  # line fingerprint
                meta_dict_b64 = fields[1]  # base64 encoded metadata dict
                ct_chunk_b64 = fields[2]  # ciphertext chunk

                # --- validate lfp, continue if failed
                lfp_check = hashlib.sha3_256(meta_dict_b64 + ct_chunk_b64).hexdigest().encode("ascii")
                if lfp != lfp_check:
                    print(f"Invalid frame: LFP fail @ line starting with: {lfp[:16]} ...")
                    continue

                # --- decode meta dict
                meta_dict = {}
                try:
                    meta_dict = json.loads(b64.urlsafe_b64decode(meta_dict_b64).decode("utf-8"))
                except Exception as e:
                    raise R3D_IO_Error(f"Invalid frame: meta_dict does not decode @ Line starting with: {lfp[:16]}...")

                # --- create segment object
                ct_seg = CTSegment()
                ct_seg.idx = meta_dict['i']
                ct_seg.parent_obj_id = meta_dict['o']
                ct_seg.nonce_hex = meta_dict['n']
                ct_seg.ct_chunk = b64.urlsafe_b64decode(ct_chunk_b64)

                # --- create or update vault object
                if ct_seg.parent_obj_id not in self.vibk:
                    vobj = VaultObj()
                    vobj.obj_id = ct_seg.parent_obj_id
                    vobj.ct_segments = [ct_seg]
                    self.vibk[vobj.obj_id] = vobj
                else:
                    vobj = self.vibk[ct_seg.parent_obj_id]
                    vobj.ct_segments.append(ct_seg)

                # ---

    # --------------------------------------------------------------------------------------------------------------------------
    def init_new_arkive(self):

        # special object: vault internal book keeping
        # map from oid -> vobj
        self.vibk = {}

    # --------------------------------------------------------------------------------------------------------------------------
    def put_object(self, vobj: VaultObj):
        """ Upsert object into the vault. """

        # NOTE obj id is internal to the vault, and normally its keyed using the vault key. obj id should not be used
        # outside the vault.
        # TODO hmac

        vobj.obj_id = hashlib.sha3_384(vobj.pt_data).hexdigest()

        self.vibk[vobj.obj_id] = vobj
        self.encrypt_vobj(vobj)

        # TODO: scan vpns for duplicates, and if found, drop old vobj (upsert logic)

    # --------------------------------------------------------------------------------------------------------------------------
    def encrypt_vobj(self, vobj: VaultObj):
        """ Encrypt the vault object using the vault key. """

        if vobj.pt_data is None:
            raise R3D_IO_Error("Vault object has no plaintext data to encrypt.")

        chunk_size = _rvcc.default_chunk_size

        for i in range(0, len(vobj.pt_data), chunk_size):
            pt_chunk = vobj.pt_data[i:i + chunk_size]

            ct_seg = CTSegment()
            ct_seg.idx = i
            ct_seg.ct_chunk = b64.urlsafe_b64encode(pt_chunk)  # TODO encrypt this chunk using the vault key
            ct_seg.nonce_hex = os.urandom(16).hex()
            ct_seg.parent_obj_id = vobj.obj_id

            vobj.ct_segments.append(ct_seg)

    # --------------------------------------------------------------------------------------------------------------------------
    def save_vault(self, output_pathname: str):
        """ Save this vault to the output file. """

        with open(output_pathname, "wb") as fh:
            for vobj in self.vibk.values():
                for ct_seg in vobj.ct_segments:
                    meta_dict = {
                        "i": ct_seg.idx,  # starting offset of the chunk in the original file
                        "o": ct_seg.parent_obj_id,
                        "n": ct_seg.nonce_hex
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

                # --- flush for each vobj
                fh.flush()
        # ---


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
