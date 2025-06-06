""" dbg_utilz.py
helper functions for debugging and testing purposes. None of this should to be imported or used by the library itself.


"""

import os
import io
import json
import hashlib
import hmac

import base64 as b64

from nacl.secret import SecretBox

from libr3dv1t.central_config import dfcc
from libr3dv1t.errors import R3D_IO_Error, R3D_V1T_Error
from libr3dv1t.typedefs import MemObj, CTSegment, RVKryptMode
from libr3dv1t.krypt_utilz import kdf
from libr3dv1t.vault.vvfs import VaultVirtualFS, VirtualFile
from libr3dv1t.log_utilz.log_man import current_logger as log
#from libr3dv1t.krypt_utilz.nonce_gen import make_nonce

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_vlt_password = b"change_me"
_vks = kdf.vks_set_from_user_pass(_vlt_password)


# mostly copied from VaultMan.process_frame_line
def unpack_frame_line(line: bytes):

    fields = line.strip().split(b'|')
    if len(fields) != 2:
        raise R3D_V1T_Error(f"Invalid frame line @ line starting with: {line[:16]}")

    meta_dict_b64 = fields[0]
    ct_chunk_b64 = fields[1]

    # --- decode meta dict
    meta_dict = {}
    try:
        meta_dict = json.loads(b64.urlsafe_b64decode(meta_dict_b64).decode("utf-8"))
    except Exception as e:
        raise R3D_V1T_Error(f"Invalid frame: meta_dict does not decode @ Line starting with: {line[:16]}")

    # --- check frame hmac
    if 'h' not in meta_dict:
        raise R3D_V1T_Error(f"Invalid frame: no hmac in meta_dict @ Line starting with: {line[:16]}")

    frame_hmac = meta_dict['h']
    meta_dict.pop('h', None)  # remove hmac from meta_dict for hmac calculation

    frame_hmac_msg = json.dumps(meta_dict).encode("ascii") + ct_chunk_b64
    recomputed_hmac = hmac.new(key=_vks.frame_hmac_key, msg=frame_hmac_msg, digestmod=hashlib.sha3_256).hexdigest()
    if frame_hmac != recomputed_hmac:
        raise R3D_V1T_Error(f"Invalid frame: hmac mismatch @ Line starting with: {line[:16]}")

    # --- create segment object
    ct_seg = CTSegment()
    ct_seg.idx = meta_dict['i']
    ct_seg.parent_obj_id = meta_dict['o']
    ct_seg.ct_chunk_b64 = ct_chunk_b64

    if RVKryptMode.CHACHA20_POLY1305.value in meta_dict:
        ct_seg.km = RVKryptMode.CHACHA20_POLY1305
        ct_seg.km_data = meta_dict[RVKryptMode.CHACHA20_POLY1305.value]
    elif RVKryptMode.FERNET.value in meta_dict:
        ct_seg.km = RVKryptMode.FERNET
        ct_seg.km_data = meta_dict[RVKryptMode.FERNET.value]
    else:
        raise R3D_V1T_Error(f"Invalid frame: unknown krypt mode @ Line starting with: {line[:16]}")

    # ---
    return ct_seg





