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

        # 'i' key in meta_dict - offset of this segment in the original file
        self.idx = idx

        # 'o' key in meta_dict - the object id of the parent vault object this segment belongs to.
        self.parent_obj_id = ''  

        # krypt mode for this segment, e.g. 'km_1' or 'km_2' - one of these strings will be present in the meta_dict
        self.km = None

        # 'km_1' or 'km_2' ... key in meta_dict - value for this key will be this dict. which contains data specific to this km
        self.km_data = {}

        # not in meta_dict, ct_chunk is the frame payload.
        self.ct_chunk = ct_chunk  # ciphertext segment
    
    def __str__(self):
        " str rep for debugging purposes. "

        return f"CTSegment: \n" \
               f"idx={self.idx}, \n" \
               f"parent_obj_id='{self.parent_obj_id}', \n" \
               f"km='{self.km.value if self.km else None}', \n" \
               f"km_data={self.km_data}, \n" \
               f"ct_chunk='{self.ct_chunk.hex()[:5]}...'\n"

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
