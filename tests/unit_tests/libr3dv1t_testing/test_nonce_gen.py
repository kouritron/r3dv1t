# -*- coding: utf-8 -*-

import os
import sys
import random
import unittest
import subprocess as sp
from pathlib import Path

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_repo_root = sp.check_output("git rev-parse --show-toplevel", shell=True).strip().decode('utf8')
_include_search_path = str((Path(_repo_root) / 'src').resolve())

if _include_search_path not in sys.path:
    sys.path.insert(0, _include_search_path)

from libr3dv1t.krypt_utilz import nonce_gen


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class TestNonceGen(unittest.TestCase):

    def test_correct_size(self):
        for i in range(16, 160):
            self.assertEqual(len(nonce_gen.make_nonce(size=i)), i)

    def test_no_repeat(self):
        """ Test that the nonce generator does not repeat nonces. """

        seen_nonces = set()
        for i in range(1000):
            nonce = nonce_gen.make_nonce(size=random.randint(16, 160))
            self.assertNotIn(nonce, seen_nonces, f"Nonce {nonce.hex()} was repeated.")
            seen_nonces.add(nonce)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    unittest.main()
