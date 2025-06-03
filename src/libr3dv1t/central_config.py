# -*- coding: utf-8 -*-
"""
Central configuration for the library.
Also documentation for the library params might be found here.
"""

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
_DEFAULT_CHUNK_SIZE = 2048
_DEFAULT_REPLICATION = 3

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class CentralConfig:
    """ Central configuration for the library.
    """

    def __init__(self):
        self.default_replicas = _DEFAULT_REPLICATION
        self.default_chunk_size = _DEFAULT_CHUNK_SIZE

        # implement any env variable overrides here

        self.dev = True


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

default_rvcc = CentralConfig()


