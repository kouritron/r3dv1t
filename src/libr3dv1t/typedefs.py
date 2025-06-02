from enum import Enum


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class VaultObj:
    """ Data class ish tracking all object attributes that r3dv1t can track.
    Try to use it as a data class and ideally avoid storing logic in this class. """

    def __init__(self, vpn: str = "", obj_mtime: float = 0.0, obj_id: str = ""):
        # vpn: vault path name, this is the name of the object in the vault.
        self.vpn = vpn
        self.obj_mtime = obj_mtime
        self.obj_id = obj_id
        self.pt_data = None
        self.ct_segments = []

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class CTSegment:
    """ Data class ish tracking a segment of a file stored in the vault. """

    def __init__(self, idx: int = 0, ct_chunk: bytes = b""):
        self.idx = idx
        self.ct_chunk = b''
        self.nonce_hex = ''  # store as hex encoded string, not raw bytes so it be serialized into json.
        self.parent_obj_id = ''  # the object id of the parent vault object this segment belongs to.


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class SegmentKryptMode(Enum):
    CHACHA20_POLY1305 = "km_1"
    FERNET = "km_2"

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class VaultKeys:
    """ Data class ish tracking the different crypto keys used by the vault. """

    def __init__(self):

        # object store fingerprinting key
        self.osfp_key = b''

        # segment keys for different encryption methods
        self.sgk_chacha20_poly1305 = b''
        self.sgk_fernet = b''
