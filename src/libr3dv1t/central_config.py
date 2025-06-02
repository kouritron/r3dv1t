# -*- coding: utf-8 -*-
"""
Central configuration for the library.
Also documentation for the library params might be found here.
"""

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
_DEFAULT_CHUNK_SIZE = 2048
_DEFAULT_REPLICATION = 3
_R3DV1T_SALT = b"libr3dv1t_salt_4242"

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class CentralConfig:
    """ Central configuration for the library.
    """

    def __init__(self):
        self.default_replicas = _DEFAULT_REPLICATION
        self.default_chunk_size = _DEFAULT_CHUNK_SIZE
        self.r3dv1t_salt = _R3DV1T_SALT

        # implement any env variable overrides here

        self.dev = True


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

default_rvcc = CentralConfig()


