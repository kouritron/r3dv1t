import os
import io
import sys
import json
import random
from pathlib import Path
import hashlib
import subprocess as sp

import gc
import traceback

from libr3dv1t.central_config import default_rvcc as _rvcc
from libr3dv1t import wire_toolz

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
_REPO_ROOT_PATH = Path(sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def rv2file():

    mem_fh = io.BytesIO()
    frame_lines = []
    frame_lines_dedup = []

    # -------------------- read the file
    with open(_REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.jpg.r3dv1t", "rb") as fh:
        frame_lines = fh.readlines()
        print(f"read # lines: {len(frame_lines)}")

        frame_lines_dedup = list(set(frame_lines))
        print(f"# dedup lines: {len(frame_lines_dedup)}")

    gc.collect()

    # -------------------- decode the frame lines
    for frame_line in frame_lines_dedup:
        try:
            df = wire_toolz.decode_frame_line(frame_line)
            # print(f"seeking to idx: { df['idx']}")
            mem_fh.seek(df['meta_dict']['i'])
            mem_fh.write(df['chunk'])
        except Exception as e:
            # TODO: put a warn in the log
            print(repr(e))
            # print(traceback.format_exc())

    # -------------------- save mem file to disk
    mem_fh.seek(0)
    with open(_REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.rcvrd.jpg", "wb") as dest_fh:
        # TODO: make this read happen in chunks to prevent holding 2 copies of the file in memory
        bytes_written_dest_file = dest_fh.write(mem_fh.read())
        dest_fh.flush()
        # print(f"mem_fh size: {mem_fh.tell()}")
        print(f"dest file bytes written: {bytes_written_dest_file}")

    mem_fh.close()
    gc.collect()
    # ---


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def file2rv():

    frame_lines = []
    src_fc = None

    with open(_REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.jpg", "rb") as fh:
        src_fc = fh.read()

    # ---
    chunk_size = _rvcc.default_chunk_size
    chunk_size = 120

    for i in range(0, len(src_fc), chunk_size):
        chunk = src_fc[i:i + chunk_size]
        frame_line = wire_toolz.make_frame_line(chunk=chunk, idx=i)
        # print(frame_line)
        frame_lines.append(frame_line)

    total_bytes_written = 0
    with open(_REPO_ROOT_PATH / "sample_data" / "gignr" / "kk.jpg.r3dv1t", "wb") as dest_fh:
        for frame_line in frame_lines:
            total_bytes_written += dest_fh.write(frame_line)
            dest_fh.flush()
        for frame_line in frame_lines:
            total_bytes_written += dest_fh.write(frame_line)
            dest_fh.flush()

    print(f"total_bytes_written: {total_bytes_written}")


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    # file2rv()
    rv2file()
