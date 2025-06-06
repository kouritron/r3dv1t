import os
import sys

from .base import LOG_RECORD, LGLVL, mk_log_record
from .base import ANSI_GREEN, ANSI_YELLOW, ANSI_RED, ANSI_RESET


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class LogStdio:

    def __init__(self):

        # --- default log level
        self.current_log_level = LGLVL.INFO

    # --------------------------------------------------------------------------------------------------------------------------
    def set_log_level(self, level):

        if not isinstance(level, LGLVL):
            raise ValueError(f"Expected an instance of LGLVL, got {type(level)}")

        self.current_log_level = level
        self.info(f"Log level changed to {level}")

    # --------------------------------------------------------------------------------------------------------------------------
    def _process_log_record(self, lgr: LOG_RECORD):

        # func_name = lgr.func_name
        fbasename = os.path.basename(lgr.filename)

        # lgr.lgr_time_ns is nanosecond. we need less.
        time_seconds = lgr.lgr_time_ns / 1_000_000_000.0  # convert to seconds
        time_trunc = f"{time_seconds:.6f}"[6:]
        msg_builder = f"{time_trunc}|{fbasename}:{lgr.line_no}|{lgr.msg}"

        if lgr.msg_lvl == LGLVL.DBUG:
            msg_builder = f'DBUG|{msg_builder}'

        if lgr.msg_lvl == LGLVL.INFO:
            msg_builder = f'{ANSI_GREEN}INFO|{msg_builder}{ANSI_RESET}'

        if lgr.msg_lvl == LGLVL.WARN:
            msg_builder = f'{ANSI_YELLOW}WARN|{msg_builder}{ANSI_RESET}'

        if lgr.msg_lvl == LGLVL.ERRR:
            msg_builder = f'{ANSI_RED}ERRR|{msg_builder}{ANSI_RESET}'

        if lgr.msg_lvl.value >= self.current_log_level.value:
            print(msg_builder, file=sys.stderr)

    # --------------------------------------------------------------------------------------------------------------------------
    def dbg(self, msg: str = ''):
        lgr = mk_log_record(msg_lvl=LGLVL.DBUG, msg=msg)
        self._process_log_record(lgr)

    def info(self, msg: str = ''):
        lgr = mk_log_record(msg_lvl=LGLVL.INFO, msg=msg)
        self._process_log_record(lgr)

    def warn(self, msg: str = ''):
        lgr = mk_log_record(msg_lvl=LGLVL.WARN, msg=msg)
        self._process_log_record(lgr)

    def err(self, msg: str = ''):
        lgr = mk_log_record(msg_lvl=LGLVL.ERRR, msg=msg)
        self._process_log_record(lgr)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------

