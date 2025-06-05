''' typedefs.py

structs, typedefs, dataclasses, enums .... used in the libr3dv1t library.

Try to avoid logic in this file as much as possible. Most of the classes here are to be treated
as data containers/data classes, not grouping of data and logic.


'''

from enum import Enum
from libr3dv1t.central_config import default_rvcc as _rvcc

_ = """
TODO:

deal with 
- vpn or vname: vault path name
- same place should handle obj_mtime



"""


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class MemObj:
    """ Data class ish tracking a r3dv1t object in memory. """

    def __init__(self):

        self.obj_id: str = ''
        self.pt_data: bytes = b''
        self.ct_segments: list[CTSegment] = []


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class CTSegment:
    """ Data class ish tracking a segment of a file stored in the vault. """

    def __init__(self, idx: int = 0, ct_chunk: bytes = b""):

        # 'i' key in meta_dict - offset of this segment in the original file
        self.idx: int = idx

        # 'o' key in meta_dict - the object id of the parent vault object this segment belongs to.
        self.parent_obj_id: str = ''

        # krypt mode for this segment, e.g. 'km_1' or 'km_2' - one of these strings will be present in the meta_dict
        self.km: RVKryptMode | None = None

        # 'km_1' or 'km_2' ... key in meta_dict - value for this key will be this dict. which contains data specific to this km
        self.km_data: dict = {}

        # not in meta_dict, ct_chunk is the frame payload.
        self.ct_chunk: bytes = ct_chunk  # ciphertext segment

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
    """ Enum for the different encryption modes used in the vault. """

    # PT = "km_0"  # plaintext, no encryption
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

        # frame line tagging key
        self.frame_hmac_key = b''

        # segment key for chacha20_poly1305 encryption
        self.sgk_chacha20 = b''

        # segment key for fernet encryption
        self.sgk_fernet = b''

    def __str__(self):
        " str rep for debugging purposes. "

        result = "VaultKeys(xxx)"

        if _rvcc.dbg_mode:
            result =  f"VaultKeys: \n" \
               f"osfp_key       = '{self.osfp_key.hex()[:4]}...', \n" \
               f"frame_hmac_key = '{self.frame_hmac_key.hex()[:4]}...'\n" \
               f"sgk_chacha20   = '{self.sgk_chacha20.hex()[:4]}...', \n" \
               f"sgk_fernet     = '{self.sgk_fernet.hex()[:4]}...'\n"

        return result
