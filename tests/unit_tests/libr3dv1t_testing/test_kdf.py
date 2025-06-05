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
test_upw_1_mvk_prefix = "53d17805d1060a7a"
test_upw_1_osfp_prefix = "bfd6b76fe1bb9fd3"
test_upw_1_frame_hmac_prefix = "bb66b271e7b8c3c2"
test_upw_1_chacha20_prefix = "4137c0ec4f64bd16"
test_upw_1_fernet_prefix = "1cb9f38b4b831a4f"


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
        self.assertEqual(actual_dk1[:len(test_upw_1_mvk_prefix)], test_upw_1_mvk_prefix)
        # print(f"actual_dk1: {actual_dk1}")

    # --------------------------------------------------------------------------------------------------------------------------
    def test_mvk_is_deterministic(self):
        run1 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()
        run2 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()
        run3 = kdf._derive_master_vault_key_from_user_pass(upw=test_upw_1).hex()

        self.assertEqual(run1, run2)
        self.assertEqual(run1, run3)

    # --------------------------------------------------------------------------------------------------------------------------
    def test_vks_known_values(self):

        vks = kdf.vks_set_from_user_pass(upw=test_upw_1)

        # --- check key prefixes
        self.assertEqual(vks.osfp_key.hex()[:len(test_upw_1_osfp_prefix)], test_upw_1_osfp_prefix)
        self.assertEqual(vks.frame_hmac_key.hex()[:len(test_upw_1_frame_hmac_prefix)], test_upw_1_frame_hmac_prefix)
        self.assertEqual(vks.sgk_chacha20.hex()[:len(test_upw_1_chacha20_prefix)], test_upw_1_chacha20_prefix)
        self.assertEqual(vks.sgk_fernet.hex()[:len(test_upw_1_fernet_prefix)], test_upw_1_fernet_prefix)

    # --------------------------------------------------------------------------------------------------------------------------
    def test_vks(self):

        vks = kdf.vks_set_from_user_pass(upw=test_upw_1)

        self.assertIsNotNone(vks)
        self.assertIsNotNone(vks.osfp_key)
        self.assertIsNotNone(vks.frame_hmac_key)
        self.assertIsNotNone(vks.sgk_chacha20)
        self.assertIsNotNone(vks.sgk_fernet)

        # --- check keys are bytes
        self.assertIsInstance(vks.osfp_key, bytes)
        self.assertIsInstance(vks.frame_hmac_key, bytes)
        self.assertIsInstance(vks.sgk_chacha20, bytes)
        self.assertIsInstance(vks.sgk_fernet, bytes)

        # --- check keys are not too short
        self.assertGreater(len(vks.osfp_key), 16)
        self.assertGreater(len(vks.frame_hmac_key), 16)
        self.assertGreater(len(vks.sgk_chacha20), 16)
        self.assertGreater(len(vks.sgk_fernet), 16)

        # --- check key lengths
        self.assertEqual(len(vks.osfp_key), 32)
        self.assertEqual(len(vks.frame_hmac_key), 32)
        self.assertEqual(len(vks.sgk_chacha20), 32)
        self.assertEqual(len(vks.sgk_fernet), 32)

        # --- check keys are not duplicated
        distinct_keys = set()
        distinct_keys.add(vks.osfp_key.hex())
        distinct_keys.add(vks.frame_hmac_key.hex())
        distinct_keys.add(vks.sgk_chacha20.hex())
        distinct_keys.add(vks.sgk_fernet.hex())

        self.assertEqual(len(distinct_keys), 4, "Vault keys should be distinct.")
        # print(f"Vault keys: {vks}")

    # --------------------------------------------------------------------------------------------------------------------------
    def test_vks_are_deterministic(self):

        vks1 = kdf.vks_set_from_user_pass(upw=test_upw_1)
        vks2 = kdf.vks_set_from_user_pass(upw=test_upw_1)

        self.assertEqual(vks1.osfp_key, vks2.osfp_key)
        self.assertEqual(vks1.frame_hmac_key, vks2.frame_hmac_key)
        self.assertEqual(vks1.sgk_chacha20, vks2.sgk_chacha20)
        self.assertEqual(vks1.sgk_fernet, vks2.sgk_fernet)


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    unittest.main()
