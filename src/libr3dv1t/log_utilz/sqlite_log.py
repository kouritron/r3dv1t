"""
A simple logging system with a sqlite log sink.

- Code over Configuration. Code is self-describing and powerful.
- Switch between views to see different log levels.

"""

import os
import sys
from pathlib import Path
import sqlite3

from libr3dv1t.log_utilz.log_common import LGLVL, LOG_RECORD, mk_log_record
from libr3dv1t.log_utilz.log_common import ANSI_GREEN, ANSI_YELLOW, ANSI_RED, ANSI_RESET


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def _process_log_record(lgr: LOG_RECORD):
    pass

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------- module api
def dbg(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.DBUG, msg=msg)
    _process_log_record(lgr)


def info(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.INFO, msg=msg)
    _process_log_record(lgr)


def warn(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.WARN, msg=msg)
    _process_log_record(lgr)


def err(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.ERRR, msg=msg)
    _process_log_record(lgr)
