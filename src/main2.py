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

# do not import MemObj here, thats internal to the vault. this file is place holder for the UI to come.
# from libr3dv1t.typedefs import MemObj

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def load_ark():
    ark_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t"
    xtract_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t.xtracted"

    demo_vm = VaultMan(vlt_file_pathname_to_load=ark_pathname)
    demo_vm.xtract_vlt_to_path(xtraction_path=xtract_pathname)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def make_ark():

    output_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t"
    kk_file_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.jpg"
    # kk_file_mtime = os.path.getmtime(kk_file_pathname)

    # -------------------- read sample file
    with open(kk_file_pathname, "rb") as fh:
        kk_fc = fh.read()

    # -------------------- create the vault manager
    test_vman = VaultMan()

    # -------------------- put things into the vault
    # vopn or vpn can be supplied later to vman, as additional parameter to put_object
    test_vman.put_object(pt_data=b"this is a test file\n", vopn='1__test.txt')
    test_vman.put_object(pt_data=kk_fc, vopn="kk.jpg")
    test_vman.put_object(pt_data=b"test 33333333333\n\n", vopn='3__test.txt')

    test_vman.save_vault(output_pathname)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    make_ark()
    load_ark()
