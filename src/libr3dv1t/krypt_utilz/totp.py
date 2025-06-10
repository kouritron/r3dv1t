import hmac
import hashlib
import time
import struct
import base64 as b64

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# Example TOTP URI format:
# otpauth://totp/<Issuer>:<AccountName>?secret=<Base32Secret>&issuer=<Issuer>&algorithm=<Algorithm>&digits=<Digits>&period=<Period>
# algorithm=SHA1 (default), SHA256, SHA512
# digits=6 (default), 8
# period=30 (default), 60 ...

_xmpl1 = "otpauth://totp/MyApp:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=MyApp"
_xmpl2 = "otpauth://totp/ExampleApp:alice@example.com?secret=JBSWY3DPEHPK3PXP&issuer=ExampleApp&algorithm=SHA1&digits=6&period=30"

_b32_secret = "JBSWY3DPEHPK3PXP" 


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def compute_totp(b32_secret, time_step=30, digits=6, alg="sha1"):

    # current window number
    win_num = int(time.time() // time_step)

    # pack window number, big endian 8 byte unsigned integer
    win_num_bytes = struct.pack(">Q", win_num)

    secret_bytes = b64.b32decode(b32_secret)

    if alg == "sha1":
        md = hmac.new(secret_bytes, win_num_bytes, hashlib.sha1).digest()
    elif alg == "sha256":
        md = hmac.new(secret_bytes, win_num_bytes, hashlib.sha256).digest()
    elif alg == "sha512":
        md = hmac.new(secret_bytes, win_num_bytes, hashlib.sha512).digest()
    else:
        raise ValueError("Unsupported hash algorithm")

    # --- dynamic truncation step (RFC 4226)
    offset = md[-1] & 0x0F
    binary = (md[offset] & 0x7F) << 24 | (md[offset + 1] & 0xFF) << 16 | (md[offset + 2] & 0xFF) << 8 | (md[offset + 3] & 0xFF)
    otp = binary % (10**digits)
    return f"{otp:0{digits}d}"


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def dbg():
    print(compute_totp(_b32_secret))
