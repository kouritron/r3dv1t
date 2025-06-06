""" vvfs.py

vvfs: vault virtual file system. vvfs tracks filenames and associations between virtual files in the vault with
objects stored in the vault object store.

Objects are always tracked with their oid, which is a keyed fingerprint.
1 or more filenames (virtual vault objects) can point to the same underlying oid.


TODO vault paths
look into leadning /
we may or may not want to remove that here.

-  I think UI should just disallow starting / in object names.
if user created a folder hierarchy like

/foo/bar.txt

the corresponding pname would be:
'foo/' + 'bar.txt'

** NOTE this might change


"""

import posixpath

from libr3dv1t.log_utilz.log_man import default_logger as log
from libr3dv1t.errors import R3D_V1T_Error


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# this will have data and logic, not good fit for typedefs.
class VirtualFile:

    def __init__(self, pname: str):
        self.pname: str = posixpath.normpath(pname)

    def __str__(self):
        return f"VirtualFile(pname={self.pname})"

    def __eq__(self, other):
        if not isinstance(other, VirtualFile):
            return False
        return self.pname == other.pname


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
    def clean_up_orphaned_oids(self):
        """ Clean up orphaned oids. An oid is considered orphaned if there are no virtual files pointing to it. """

        log.dbg("clean_up_orphaned_oids: start")
        orphaned_oids = []

        # find all oids that have no virtual files pointing to them
        for oid, vfiles in self.oid_to_vf.items():
            if not vfiles:
                orphaned_oids.append(oid)

        # remove orphaned oids from the map
        for orphaned_oid in orphaned_oids:
            log.info(f"clean_up_orphaned_oids: Removing orphaned oid '{orphaned_oid}'.")
            del self.oid_to_vf[orphaned_oid]

    # --------------------------------------------------------------------------------------------------------------------------
    def link_vf(self, vf: VirtualFile, oid: str):
        """ Link a virtual file to an oid. This means that the virtual file points to the object with this oid. """

        if not isinstance(vf, VirtualFile):
            raise R3D_V1T_Error(f"VaultVirtualFS.link_vf: vf must be VirtualFile, got {type(vf)}.")
        if not isinstance(oid, str):
            raise R3D_V1T_Error(f"VaultVirtualFS.link_vf: oid must be str, got {type(oid)}.")

        log.info(f"link_vf: '{vf}' <---> '{oid}'")

        run_oid_clean_up = False

        # if vf.pname already points to some oid, we need to remove that association first
        for existing_oid, vfiles in self.oid_to_vf.items():
            for existing_vf in vfiles:
                if existing_vf == vf:
                    log.info(f"link_vf: Removing existing association for '{vf}' with oid '{existing_oid}'.")
                    vfiles.remove(existing_vf)
                    # this might create orphaned oids
                    if not vfiles:
                        run_oid_clean_up = True

        # --- clean up orphaned oids if needed
        if run_oid_clean_up:
            self.clean_up_orphaned_oids()

        # now we can add the new association
        if oid in self.oid_to_vf:
            self.oid_to_vf[oid].append(vf)
        else:
            self.oid_to_vf[oid] = [vf]

    # --------------------------------------------------------------------------------------------------------------------------
    def unlink_vf(self, vf: VirtualFile):
        """ Unlink aka delete a virtual file in this vvfs. if oids become orphaned, they will be cleaned up. """

        if not isinstance(vf, VirtualFile):
            raise R3D_V1T_Error(f"VaultVirtualFS.unlink_vf: vf must be VirtualFile, got {type(vf)}.")

        log.dbg(f"unlink_vf: '{vf.pname}'")
        run_oid_clean_up = False

        # find the oid that this virtual file points to and remove the association
        for oid, vfiles in self.oid_to_vf.items():
            for existing_vf in vfiles:
                if existing_vf == vf:
                    log.info(f"unlink_vf: Removing association for '{vf.pname}' with oid '{oid}'.")
                    vfiles.remove(existing_vf)
                    # this might create orphaned oids
                    if not vfiles:
                        run_oid_clean_up = True

        # --- clean up orphaned oids if needed
        if run_oid_clean_up:
            self.clean_up_orphaned_oids()

    # --------------------------------------------------------------------------------------------------------------------------
    def get_oid(self, vf: VirtualFile) -> str:
        """ Get the oid for a given virtual file path name. """

        log.dbg(f"get_oid({vf})")

        for oid, vfiles in self.oid_to_vf.items():
            for existing_vf in vfiles:
                if existing_vf == vf:
                    log.info(f"get_oid: Found oid='{oid}' for '{vf}'.")
                    return oid

        raise R3D_V1T_Error(f"get_oid: {vf} not found.")

    # --------------------------------------------------------------------------------------------------------------------------
    def get_vf_by_oid(self, oid: str) -> str:
        """ Get the vf objects that point to this oid. """

        log.dbg(f"get_vf_by_oid: '{oid}'")

        if oid in self.oid_to_vf:
            log.info(f"get_vf_by_oid: Found {len(self.oid_to_vf[oid])} virtual files for oid '{oid}'.")
            return self.oid_to_vf[oid]

        raise R3D_V1T_Error(f"get_vf_by_oid: oid='{oid}' not found.")
