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
from libr3dv1t.typedefs import MemObj

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
    demo_vm = VaultMan()

    # -------------------- put things into the vault
    mobj1 = MemObj()
    mobj1.pt_data = b"this is a test file\n"
    demo_vm.put_object(mobj1)

    mobj2 = MemObj()
    mobj2.pt_data = kk_fc
    demo_vm.put_object(mobj2)

    mobj3 = MemObj()
    mobj3.pt_data = b"test 33333333333\n\n"
    demo_vm.put_object(mobj3)
    # mobj3.vpn = "3_test_33.txt"

    demo_vm.save_vault(output_pathname)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    make_ark()
    load_ark()
