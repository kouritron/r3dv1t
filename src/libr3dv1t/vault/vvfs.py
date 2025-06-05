""" vvfs.py

vvfs: vault virtual file system. vvfs tracks filenames and associations between virtual files in the vault with
objects stored in the vault object store.

Objects are always tracked with their oid, which is a keyed fingerprint.
1 or more filenames (virtual vault objects) can point to the same underlying oid.


TODO vault paths
For example:
/aaa.txt means an object called aaa.txt stored at the root of the vault.


"""

from libr3dv1t.log_utilz.log_man import current_logger as log


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class VVFS:
    """ A bidirectional map between vopn and object ids. """

    def __init__(self):
        """ Initialize a new VVFS. """

        self.vopn2oid = {}
        self.oid2vopn = {}
        log.dbg("New VVFS initialized.")

    def upsert_vopn(self, vopn: str, oid: str):
        """ Upsert a <vopn, oid> row in to this vopn map.
        - If vopn already exists, it will point to new oid --- old oid will be removed from the map. 
        """

        log.dbg(f"upsert_vopn: '{vopn}' <---> '{oid}'")

        if vopn in self.vopn2oid:
            old_oid = self.vopn2oid[vopn]
            del self.oid2vopn[old_oid]

        self.vopn2oid[vopn] = oid
        self.oid2vopn[oid] = vopn

    def get_oid(self, vopn: str) -> str:
        return self.vopn2oid.get(vopn)

    def get_vopn(self, oid: str) -> str:
        return self.oid2vopn.get(oid)
