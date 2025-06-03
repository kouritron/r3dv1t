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
        self.idx = idx  # offset of this segment in the original file
        self.ct_chunk = ct_chunk  # ciphertext segment
        self.parent_obj_id = ''  # the object id of the parent vault object this segment belongs to.
        self.km_data = {}  # a dict to hold additional data for the segment relevant to the encryption mode.
        self.km = None  # encryption mode used for this segment

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class RVKryptMode(Enum):
    CHACHA20_POLY1305 = "km_1"
    FERNET = "km_2"
    # TODO: look into github.com/tink-crypto/tink-py

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

    def __str__(self):
        " str rep for debugging purposes. "

        return f"VaultKeys: \n" \
               f"osfp_key='{self.osfp_key.hex()[:5]}...', \n" \
               f"sgk_chacha20_poly1305='{self.sgk_chacha20_poly1305.hex()[:5]}...', \n" \
               f"sgk_fernet='{self.sgk_fernet.hex()[:5]}...'\n"
