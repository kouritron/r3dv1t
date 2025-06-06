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
import shutil

from libr3dv1t.central_config import dfcc
from libr3dv1t.vault.vault_man import VaultMan
from libr3dv1t.log_utilz.log_man import default_logger as log

# do not import MemObj here, thats internal to the vault. this file is place holder for the UI to come.
# from libr3dv1t.typedefs import MemObj

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def refresh_sample_data_folder():
    log.info("refresh_sample_data_folder")

    tmp_path = _REPO_ROOT_PATH / "sample_data" / "gignr"

    # drop tmp_path if it exists
    if tmp_path.exists():
        shutil.rmtree(tmp_path)

    # create tmp_path folder
    tmp_path.mkdir(parents=True, exist_ok=True)

    # kk.jpg into tmp_path
    kk_file_pathname = _REPO_ROOT_PATH / "sample_data" / "kk.jpg"
    shutil.copy(kk_file_pathname, tmp_path / "kk.jpg")


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def load_ark():
    print("\n\n\n\n")
    log.info("load_ark")

    ark_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t"
    xtract_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t.xtracted"

    demo_vm = VaultMan(vlt_password=b"change_me", vlt_file_pathname_to_load=ark_pathname)
    demo_vm.xtract_vlt_to_path(xtraction_path=xtract_pathname)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def make_ark():
    print("\n\n\n\n")
    log.info("make_ark")

    output_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "test.r3dv1t"
    kk_file_pathname = _REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.jpg"
    # kk_file_mtime = os.path.getmtime(kk_file_pathname)

    # -------------------- read sample file
    with open(kk_file_pathname, "rb") as fh:
        kk_fc = fh.read()

    # -------------------- create the vault manager
    test_vman = VaultMan(vlt_password=b"change_me")

    # -------------------- put things into the vault
    # vopn or vpn can be supplied later to vman, as additional parameter to put_object
    test_vman.put_object(pt_data=b"this is a test file\n", virt_name='1__test.txt')
    test_vman.put_object(pt_data=kk_fc, virt_name="kk.jpg")
    test_vman.put_object(pt_data=b"test 33333333333\n\n", virt_name='3__test.txt')

    test_vman.save_vault(output_pathname)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    refresh_sample_data_folder()
    make_ark()
    load_ark()
