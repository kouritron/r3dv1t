# -*- coding: utf-8 -*-
import os
import sys
import unittest
import subprocess as sp
from pathlib import Path

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
_repo_root = sp.check_output("git rev-parse --show-toplevel", shell=True).strip().decode('utf8')
_include_search_path = str((Path(_repo_root) / 'src').resolve())

if _include_search_path not in sys.path:
    sys.path.insert(0, _include_search_path)

from libr3dv1t.krypt_utilz import kdf
# you could put a utilz.py in the same dir as this file, and import from it like this
# from .utilz import foo22

# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------- test data
test_upw_1 = b"change_me"
xpected_mvk_prefix = "4467880d3ad5aab"


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class TestKDF(unittest.TestCase):

    def setUp(self):
        """ Set up the test environment. """
        # This method is called before each test method.
        # You can use it to set up any state you want to share across tests.
        pass

    def tearDown(self):
        """ Clean up after each test. """
        # This method is called after each test method.
        # You can use it to clean up any state you want to reset.
        pass

    # --------------------------------------------------------------------------------------------------------------------------
    def test_mvk_known_values(self):

        actual_dk1 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()
        self.assertEqual(actual_dk1[:len(xpected_mvk_prefix)], xpected_mvk_prefix)

    def test_mvk_is_deterministic(self):
        run1 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()
        run2 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()
        run3 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()

        self.assertEqual(run1, run2)
        self.assertEqual(run1, run3)

    # --------------------------------------------------------------------------------------------------------------------------
    def test_vks(self):

        vks = kdf.vks_set_from_user_pass(upw=test_upw_1)

        self.assertIsNotNone(vks)
        self.assertIsNotNone(vks.osfp_key)
        self.assertIsNotNone(vks.sgk_chacha20_poly1305)
        self.assertIsNotNone(vks.sgk_fernet)

        # --- check keys are bytes
        self.assertIsInstance(vks.osfp_key, bytes)
        self.assertIsInstance(vks.sgk_chacha20_poly1305, bytes)
        self.assertIsInstance(vks.sgk_fernet, bytes)

        # --- check keys are not empty
        self.assertGreater(len(vks.osfp_key), 0)
        self.assertGreater(len(vks.sgk_chacha20_poly1305), 0)
        self.assertGreater(len(vks.sgk_fernet), 0)

        # TODO decision on key lengths
        # self.assertEqual(len(vks.osfp_key), 32)
        # self.assertEqual(len(vks.sgk_chacha20_poly1305), 32)
        # self.assertEqual(len(vks.sgk_fernet), 32)

        # --- check keys are not duplicated
        self.assertNotEqual(vks.osfp_key, vks.sgk_chacha20_poly1305)
        self.assertNotEqual(vks.osfp_key, vks.sgk_fernet)
        self.assertNotEqual(vks.sgk_chacha20_poly1305, vks.sgk_fernet)

    def test_vks_are_deterministic(self):

        vks1 = kdf.vks_set_from_user_pass(upw=test_upw_1)
        vks2 = kdf.vks_set_from_user_pass(upw=test_upw_1)

        self.assertEqual(vks1.osfp_key, vks2.osfp_key)
        self.assertEqual(vks1.sgk_chacha20_poly1305, vks2.sgk_chacha20_poly1305)
        self.assertEqual(vks1.sgk_fernet, vks2.sgk_fernet)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    unittest.main()
