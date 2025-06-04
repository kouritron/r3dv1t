""" vopn_map.py

vopn: virtual object path name. This is the path name of an object stored in the vault.

For example:
/aaa.txt means an object called aaa.txt stored at the root of the vault.

VOPNMap class is a bidirectional map between vopn and object ids.

While this allows retrieving vopn from oid, (key from value), vopn is still the key in the map.
Upsert semantics applies to vopn not oid.


"""


class VOPNMap:
    """ A bidirectional map between vopn and object ids. """

    def __init__(self):
        self.vopn_to_oid = {}
        self.oid_to_vopn = {}

    def upsert_vopn(self, vopn: str, oid: str):

        if vopn in self.vopn_to_oid:
            old_oid = self.vopn_to_oid[vopn]
            del self.oid_to_vopn[old_oid]

        self.vopn_to_oid[vopn] = oid
        self.oid_to_vopn[oid] = vopn

    def get_oid(self, vopn: str) -> str:
        return self.vopn_to_oid.get(vopn)

    def get_vopn(self, oid: str) -> str:
        return self.oid_to_vopn.get(oid)
