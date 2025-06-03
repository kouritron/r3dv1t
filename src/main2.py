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
from libr3dv1t.vault.vault_man import VaultMan
from libr3dv1t.typedefs import VaultObj
from libr3dv1t.errors import R3D_IO_Error

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def load_ark():
    ark_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t"

    demo_vm = VaultMan(vlt_file_pathname_to_load=ark_pathname)

    pass

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def make_ark():

    output_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t"
    kk_file_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.jpg"
    kk_file_mtime = os.path.getmtime(kk_file_pathname)

    # -------------------- read sample file
    with open(kk_file_pathname, "rb") as fh:
        kk_fc = fh.read()

    # -------------------- create the vault manager
    demo_vm = VaultMan()

    # -------------------- put things into the vault
    vobj1 = VaultObj(vpn="1_test.txt")
    vobj1.pt_data = b"this is a test file\n"
    demo_vm.put_object(vobj1)

    vobj2 = VaultObj(vpn="kk.jpg", obj_mtime=kk_file_mtime)
    vobj2.pt_data = kk_fc
    demo_vm.put_object(vobj2)

    vobj3 = VaultObj(vpn="3_test_33.txt")
    vobj3.pt_data = b"test 33333333333\n\n"
    demo_vm.put_object(vobj3)

    demo_vm.save_vault(output_pathname)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    # make_ark()
    load_ark()
