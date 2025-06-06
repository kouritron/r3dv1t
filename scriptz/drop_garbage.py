from pathlib import Path
import subprocess as sp
import shutil

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def drop_wsl_zone_id_bs():

    zone_files = [f for f in Path(_REPO_ROOT_PATH).rglob('*') if "Zone.Identifier" in f.name]
    for zf in zone_files:
        if zf.exists():
            print(zf)
            zf.unlink()

    print(f"Purged {len(zone_files)} Zone.Identifier files from {_REPO_ROOT_PATH}.")


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def drop_pyc_pyo_files():

    garbage_files = [f for f in Path(_REPO_ROOT_PATH).rglob('*.py[ocd]')]

    for tf in garbage_files:
        if tf.exists():
            print(tf)
            tf.unlink()

    print(f"Purged {len(garbage_files)} .pyc and .pyo files from {_REPO_ROOT_PATH}.")


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def drop_pycache_folder():

    pycache_folders = [f for f in Path(_REPO_ROOT_PATH).rglob('__pycache__')]
    for pcf in pycache_folders:
        if pcf.exists():
            print(pcf)
            shutil.rmtree(pcf)

    print(f"Purged {len(pycache_folders)} __pycache__ folders from {_REPO_ROOT_PATH}.")


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    drop_wsl_zone_id_bs()
    drop_pycache_folder()
    drop_pyc_pyo_files()
