from hashlib import pbkdf2_hmac
from hashlib import scrypt as hl_scrypt
import gc

from libr3dv1t.errors import R3D_V1T_Error
from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t.typedefs import VaultKeys


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def _derive_master_vault_key_from_user_pass(upw: bytes) -> bytes:

    if not isinstance(upw, bytes):
        raise R3D_V1T_Error("KDF: User pass must be bytes.")

    # ------------ scrypt for memory hard key derivation
    # n is the CPU/memory cost factor. must be factor of 2.
    # r is the block size.
    # p is the parallelization factor.

    # Good choice to set params to <n=2**14, r=8, p=1>   ==>>   This implies a 16 MB memory buffer.
    # Scrypt is weaker than bcrypt if buffer is under 4MB. but 16MB is pretty good.
    ik = hl_scrypt(password=upw, salt=_rvcc.r3dv1t_salt, n=2**14, r=8, p=1, dklen=160)

    ik_a = ik[:(len(ik) // 2)]
    ik_b = ik[(len(ik) // 2):]

    # ------------ now do an extra compute step using PBKDF2
    # pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)
    # dklen: 64 bytes = 512 bits
    # Given that iterations is set to 400k here, this step is probably not a good place to increase dklen.
    # if you need longer key, do another pbkdf2_hmac step.
    mvk = pbkdf2_hmac(hash_name='sha3_512', password=ik_a, salt=ik_b, iterations=420_042, dklen=64)

    return mvk


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def _vks_set_from_user_pass(upw: bytes) -> VaultKeys:

    if not isinstance(upw, bytes):
        raise R3D_V1T_Error("KDF: User pass must be bytes.")

    # ------------ step 1: get mvk
    mvk = _derive_master_vault_key_from_user_pass(upw)
    gc.collect()

    # ------------ step 2: lengthen mvk to get vk_long
    vk_long = pbkdf2_hmac(hash_name='sha3_512', password=mvk, salt=b'', iterations=42, dklen=2048)

    # ------------ create the vault keys object using vk_long
    vks = VaultKeys()

    # --- use separate 60 bytes chunks of vk_long for computing the individual vault keys, throw away the rest.
    vks.osfp_key = pbkdf2_hmac(hash_name='sha3_512', password=vk_long[100:160], salt=b'osfp', iterations=42, dklen=64)

    vks.sgk_chacha20_poly1305 = pbkdf2_hmac(hash_name='sha3_512',
                                            password=vk_long[200:260],
                                            salt=b'sgk_chacha20_poly1305',
                                            iterations=42,
                                            dklen=64)
    vks.sgk_fernet = pbkdf2_hmac(hash_name='sha3_512', password=vk_long[300:360], salt=b'sgk_fernet', iterations=42, dklen=64)

    # NOTE: feel free to add more vault keys here as needed. vk_long has plenty unused bytes left, and further increasing
    # the length of vk_long should not change earlier bytes.

    return vks


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def vks_set_from_user_pass(upw: bytes) -> VaultKeys:
    """ Derive a vault key from a user passphrase. """

    gc.collect()
    return _vks_set_from_user_pass(upw=upw)
