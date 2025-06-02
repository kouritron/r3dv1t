import os
import time
from hashlib import pbkdf2_hmac, sha3_384
from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t.errors import R3D_V1T_Error


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def make_nonce(size: int):
    """ Generate a random nonce for cryptographic operations. """

    # 24 bytes is used by pynacl for chacha20poly1305
    # disallow less than 16 bytes
    if size < 16:
        raise R3D_V1T_Error("Nonce less than 16 bytes is not allowed.")

    rand_bytes_kernel = os.urandom(80)  # 80 bytes = 640 bits
    rand_bytes_time = sha3_384(str(time.time_ns() * time.time_ns()).encode('ascii')).digest()

    combined_rand = sha3_384(rand_bytes_kernel + rand_bytes_time).digest()

    # PBKDF2 is not necessary here but its convinient to supported any requested length
    nonce = pbkdf2_hmac(hash_name='sha3_512', password=combined_rand, salt=_rvcc.r3dv1t_salt, iterations=8, dklen=size)

    return nonce
