"""
Central configuration for the library.
Also documentation for some library params might be found here.
"""
from .typedefs import RVKryptMode

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_DEFAULT_CHUNK_SIZE = 2048
_DEFAULT_REPLICATION = 3


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class CentralConfig:
    """ Central configuration for the library. """

    def __init__(self):
        self.default_replicas = _DEFAULT_REPLICATION
        self.default_chunk_size = _DEFAULT_CHUNK_SIZE

        self.default_krypt_mode = RVKryptMode.CHACHA20_POLY1305

        # implement any env variable overrides here

        self.dbg_mode = True


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------- default cc
# create default cc lazily as needed
_default_cc: CentralConfig | None = None


def dfcc() -> CentralConfig:
    """ Get the default central config. """

    global _default_cc
    if _default_cc is None:
        _default_cc = CentralConfig()
    return _default_cc
