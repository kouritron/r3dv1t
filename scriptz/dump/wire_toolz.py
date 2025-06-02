import os
import io
import sys
import json
import hashlib
import base64 as b64

from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t.errors import R3D_IO_Error

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------- r3dv1t file format
"""
This is r3dv1t file format. The outer file format is not versioned as of now, and is unlikely to need changes.
Any changes can be accommodated inside meta_dict and chunk system.

- A r3dv1t file represents the encrypted vault or archive. its an object store.
- The file is a multi line text file where each line represents a frame.

# ------------------------------------------ line spec
[lfp] | [meta_dict_b64] | [chunk or frame payload]

- lfp: line fingerprint - sha3_256 is assumed by default.
- meta_dict_b64: a base64 encoded json dict -- this is where all the extensibility is.
- chunk: This is b64 encoded frame payload

** lines maybe of any length, but for optimal performance chunk size of 2k or 4k are recommended.
** As of now i am not sure if frames with no chunk will be useful or not, they might be. Nothing disallows it.


Example lines:
0a1b2c3....d4e5f62|eyJpIjogMH0=|__muh_data__|


# ------------------------------------------ sha3_256 field
*** for line to be valid, lfp must match the recomputed value of the present fields,
which ever is present, excluding pipe and newline characters.

lfp == sha3_256(meta_dict_b64 + [chunk])


# ------------------------------------------ meta_dict_b64
** meta_dict_b64 is a base64 encoded json dict.
** meta_dict is a dict with the following fields:
- i: starting offset of the chunk in the original file
- o: object id (oid) of the original file. a hmac_sha3_384 fingerprint of the original file.
    - the fp is computed against the plaintext original file, but is keyed using one of the vault key derivations.
    - special case: if meta_dict['o'] == 'vibk', then this object is the vault internal bookkeeping object. vibk.


# ------------------------------------------ chunk
** a b64 encoded chunk of the original file whose starting offset is in the meta_dict




# ------------------------------------------ Misc notes

** base64 encoding - only 33% space penalty worth it -- 3 bytes becomes 4 bytes
this allows the output file to be a easyily readable text file.
also allows git to store the file efficiently. As objects are added/removed to/from the vault.

** b64 is always urlsafe by default unless otherwise specified.

"""


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def make_frame_line(chunk: bytes, idx: int) -> bytes:

    meta_dict = {
        'i': idx,
        'o': "TODO",
    }

    meta_dict_b64 = b64.urlsafe_b64encode(json.dumps(meta_dict).encode("utf-8"))
    chunk_b64 = b64.urlsafe_b64encode(chunk)

    # [lfp] | [meta_dict_b64] | [chunk or frame payload]

    hfunc = hashlib.sha3_256()
    hfunc.update(meta_dict_b64)
    hfunc.update(chunk_b64)
    lfp = hfunc.hexdigest().encode("ascii")

    line = lfp + b'|' + meta_dict_b64 + b'|' + chunk_b64 + b'\n'

    return line


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def decode_frame_line(line: bytes) -> dict:

    # [lfp] | [meta_dict_b64] | [chunk or frame payload in b64]
    df = {}  # decoded frame

    # -------------------- check splitable psv structure
    fields = line.strip().split(b'|')
    if len(fields) < 2:
        raise R3D_IO_Error(f"Invalid frame line at line starting with: {line[:16]}...")

    lfp_bytes = fields[0]
    meta_dict_b64 = fields[1]
    chunk_b64 = fields[2]

    try:
        df['lfp'] = lfp_bytes.decode("ascii")
    except Exception as e:
        raise R3D_IO_Error(f"Invalid frame: LFP does not decode @ line starting with: {line[:16]}...")

    # -------------------- check lfp
    hfunc = hashlib.sha3_256()
    hfunc.update(meta_dict_b64)
    hfunc.update(chunk_b64)

    lfp_check = hfunc.hexdigest()
    if df['lfp'] != lfp_check:
        raise R3D_IO_Error(f"Invalid frame: Failed LFP check. Expected fp: {df['lfp']}")

    # -------------------- decode chunk
    try:
        df['chunk'] = b64.urlsafe_b64decode(chunk_b64)
    except Exception as e:
        raise R3D_IO_Error(f"Invalid frame: Chunck does not decode @ Line starting with: {line[:16]}...")

    # -------------------- decode meta_dict
    try:
        df['meta_dict'] = json.loads(b64.urlsafe_b64decode(meta_dict_b64).decode("utf-8"))
    except Exception as e:
        raise R3D_IO_Error(f"Invalid frame: meta_dict does not decode @ Line starting with: {line[:16]}...")

    # ---
    # print(df)

    # -------------------- check meta_dict
    if _rvcc.dev:
        if 'i' not in df['meta_dict']:
            raise R3D_IO_Error(f"Invalid frame: meta_dict does not contain an idx @ Line starting with: {line[:16]}...")

        if 'o' not in df['meta_dict']:
            raise R3D_IO_Error(f"Invalid frame: meta_dict does not contain oid @ Line starting with: {line[:16]}...")

        if not isinstance(df['meta_dict']['i'], int):
            raise R3D_IO_Error(f"Invalid frame: meta_dict[i] is not an int @ Line starting with: {line[:16]}...")

        if df['meta_dict']['i'] < 0:
            raise R3D_IO_Error(f"Invalid frame: meta_dict[i] is negative @ Line starting with: {line[:16]}...")

    return df
