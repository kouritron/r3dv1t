import enum
import time
import inspect

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
ANSI_RED = "\033[31m"  # or "\u001b[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[37m"
ANSI_RESET = "\033[0m"


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class LGLVL(enum.Enum):
    DBUG = 10
    INFO = 20
    WARN = 30
    ERRR = 40

    def __str__(self):
        return super().__str__()


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class LOG_RECORD:

    def __init__(self):

        self.lgr_time_ns = time.time_ns()

        self.msg: str = ""

        # level attached to this log msg. i.e. if user said: log.dbg() then this is set to LGLVL.DEBUG
        self.msg_lvl: LGLVL

        # caller file name, line number and function name.
        self.filename: str
        self.line_no: str
        self.func_name: str

        # if needed:
        # process name, process id, thread name, thread id ....


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# --- create a log record and save as much info as possible
def mk_log_record(msg_lvl, msg=''):

    log_producer_frame_info = inspect.stack()[2]

    caller_filename = log_producer_frame_info.filename
    caller_lineno = str(log_producer_frame_info.lineno)
    caller_funcname = log_producer_frame_info.function

    lgr = LOG_RECORD()

    lgr.msg = msg
    lgr.msg_lvl = msg_lvl
    lgr.filename = caller_filename
    lgr.line_no = caller_lineno
    lgr.func_name = caller_funcname

    return lgr
