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

from libr3dv1t.central_config import dfcc
from libr3dv1t.krypt_utilz import kdf
from libr3dv1t.krypt_utilz import totp

from nacl.secret import SecretBox
from nacl.utils import random

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def main2():
    totp.dbg()



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
