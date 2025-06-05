''' kdf.py
-----
Key Derivation Function (KDF) logic for R3D Vault.
All the kdf logic must be in this file. Its the documentation and self describing source of truth for it.
No reason to move any constants or logic out of this file, as its not meant to be changed overtime.

Once v1.0 is released, ideally this file should never change again.
If there absolutely is a need to change it, then the new system could use new krypt mode numbers in RVKryptMode Enum.
'''

from hashlib import pbkdf2_hmac as _pbkdf2_hmac
from hashlib import scrypt as _hl_scrypt
import gc

from libr3dv1t.errors import R3D_V1T_Error
from libr3dv1t.typedefs import VaultKeys

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# preferred Psuedo Random Function for KDF
_PRF = 'sha3_512'


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
    ik = _hl_scrypt(password=upw, salt=b"r3dv1t_memstep_salt_42____42", n=2**14, r=8, p=1, dklen=160)

    # ------------ now do an extra compute step using PBKDF2
    # pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)
    # dklen: 64 bytes = 512 bits
    # Given that iterations is set to 400k here, this step is probably not a good place to increase dklen.
    # if you need longer key, do another pbkdf2_hmac step.
    mvk = _pbkdf2_hmac(hash_name=_PRF, password=ik, salt=b"r3dv1t_cpustep", iterations=420_042, dklen=64)

    return mvk


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def _vks_set_from_user_pass(upw: bytes) -> VaultKeys:

    if not isinstance(upw, bytes):
        raise R3D_V1T_Error("KDF: User pass must be bytes.")

    # ---------- step 1: get mvk
    mvk = _derive_master_vault_key_from_user_pass(upw)
    gc.collect()

    # ------------ step 2: lengthen mvk to get vk_long
    vk_long = _pbkdf2_hmac(hash_name=_PRF, password=mvk, salt=b'__vk__long__', iterations=42, dklen=2048)

    # ------------ create the vault keys object from vk_long
    vks = VaultKeys()

    # --- use separate 60 bytes chunks of vk_long for computing the individual vault keys, throw away the rest.
    vks.osfp_key = _pbkdf2_hmac(hash_name=_PRF, password=vk_long[100:160], salt=b'osfp', iterations=42, dklen=32)
    vks.frame_hmac_key = _pbkdf2_hmac(hash_name=_PRF, password=vk_long[200:260], salt=b'fl_hmac', iterations=42, dklen=32)
    vks.sgk_chacha20 = _pbkdf2_hmac(hash_name=_PRF, password=vk_long[300:360], salt=b'sgk_cha20', iterations=42, dklen=32)
    vks.sgk_fernet = _pbkdf2_hmac(hash_name=_PRF, password=vk_long[400:460], salt=b'sgk_fernet', iterations=42, dklen=32)

    # NOTE: feel free to add more vault keys here as needed. vk_long has plenty unused bytes left,
    # and further increasing the length of vk_long should not change earlier bytes.

    return vks


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def vks_set_from_user_pass(upw: bytes) -> VaultKeys:
    """ Derive a vault key from a user passphrase. """

    gc.collect()
    return _vks_set_from_user_pass(upw=upw)
