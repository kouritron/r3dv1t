""" vvfs.py

vvfs: vault virtual file system. vvfs tracks filenames and associations between virtual files in the vault with
objects stored in the vault object store.

Objects are always tracked with their oid, which is a keyed fingerprint.
1 or more filenames (virtual vault objects) can point to the same underlying oid.


TODO vault paths
/aaa.txt  ...


"""

from libr3dv1t.log_utilz.log_man import current_logger as log
from libr3dv1t.errors import R3D_V1T_Error

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# this will have data and logic, not good fit for typedefs.
class VirtualFile:

    def __init__(self, pname: str):

        self.pname: str = pname

    def __str__(self):
        return "TODO"


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class VaultVirtualFS:
    """  """

    def __init__(self):
        """ Initialize a new VVFS. """

        # vvfs main data structure is a map from oid to list of VirtualFile
        self.oid_to_vf: dict[str, list[VirtualFile]] = {}

        log.dbg("New VVFS initialized.")

    # --------------------------------------------------------------------------------------------------------------------------
    def create_file(self, oid: str, vf: VirtualFile):
        """  """

        log.dbg(f"create_file: '{oid}' <---> '{vf}'")

        if oid in self.oid_to_vf:
            self.oid_to_vf[oid].append(vf)
        else:
            self.oid_to_vf[oid] = [vf]

    # --------------------------------------------------------------------------------------------------------------------------
    def get_oid(self, pname: str) -> str:
        """ Get the oid for a given virtual file path name. """

        log.dbg(f"get_oid: '{pname}'")

        for oid, vfiles in self.oid_to_vf.items():
            for vf in vfiles:
                if vf.pname == pname:
                    return oid

        raise R3D_V1T_Error(f"VaultVirtualFS.get_oid: Virtual file @ pname='{pname}' not found.")

    # --------------------------------------------------------------------------------------------------------------------------
    def get_vf_by_oid(self, oid: str) -> str:
        """ Get the vf objects that point to this oid. """

        log.dbg(f"get_vf_by_oid: '{oid}'")

        if oid in self.oid_to_vf:
            return self.oid_to_vf[oid]

        raise R3D_V1T_Error(f"VaultVirtualFS.get_vf_by_oid: oid='{oid}' not found.")
