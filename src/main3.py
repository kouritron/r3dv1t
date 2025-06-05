import os
import io
import sys
import json
import random
import hashlib
import gc
import traceback
import subprocess as sp
from pathlib import Path

from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t.errors import R3D_IO_Error
from libr3dv1t.krypt_utilz import kdf
from libr3dv1t.typedefs import VaultKeys

from nacl.secret import SecretBox
from nacl.utils import random

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def main2():
    # print(os.getcwd())
    # print(kdf._derive_master_vault_key_from_user_pass(upw=b"change_me").hex())

    vks = kdf.vks_set_from_user_pass(upw=b"change_me")
    print(f"osfp_key: {vks.osfp_key.hex()}")
    print(f"frame_hmac_key: {vks.frame_hmac_key.hex()}")
    print(f"sgk_chacha20: {vks.sgk_chacha20.hex()}")
    print(f"sgk_fernet: {vks.sgk_fernet.hex()}")


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def main():
    pynacl_key = random(SecretBox.KEY_SIZE)
    pynacl_nonce = random(SecretBox.NONCE_SIZE)

    print(f"pynacl_key: {pynacl_key.hex()}")
    print(f"pynacl_nonce: {pynacl_nonce.hex()}")


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    main2()
