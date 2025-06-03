import os
import sys

from libr3dv1t.log_utilz.log_manager import LGLVL, LOG_RECORD, mk_log_record
from libr3dv1t.log_utilz.log_manager import ANSI_GREEN, ANSI_YELLOW, ANSI_RED, ANSI_RESET


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def _process_log_record(lgr: LOG_RECORD):
    """ Process the log record and print it to stdout or stderr based on the log level. """

    # func_name = lgr.func_name
    fbasename = os.path.basename(lgr.filename)

    msg_builder = f"{int(lgr.lgr_time_ns)}|{fbasename}:{lgr.line_no}|{lgr.msg}"

    if lgr.msg_lvl == LGLVL.DBUG:
        msg_builder = f'DBUG|{msg_builder}'

    if lgr.msg_lvl == LGLVL.INFO:
        msg_builder = f'{ANSI_GREEN}INFO|{msg_builder}{ANSI_RESET}'

    if lgr.msg_lvl == LGLVL.WARN:
        msg_builder = f'{ANSI_YELLOW}WARN|{msg_builder}{ANSI_RESET}'

    if lgr.msg_lvl == LGLVL.ERRR:
        msg_builder = f'{ANSI_RED}ERRR|{msg_builder}{ANSI_RESET}'

    print(msg_builder, file=sys.stderr)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------- module api
def dbg(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.DBUG, log_msg=msg)
    _process_log_record(lgr)


def info(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.INFO, log_msg=msg)
    _process_log_record(lgr)


def warn(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.WARN, log_msg=msg)
    _process_log_record(lgr)


def err(msg=None):
    lgr = mk_log_record(msg_lvl=LGLVL.ERRR, log_msg=msg)
    _process_log_record(lgr)
