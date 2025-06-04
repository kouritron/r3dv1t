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

from libr3dv1t.utilz.vopn_map import VOPNMap


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class TestVOPNMap(unittest.TestCase):

    def test_1(self):
        vopn_map = VOPNMap()

        vopn_map.upsert_vopn('aaa.txt', 'oid1')
        vopn_map.upsert_vopn('bbb.txt', 'oid2')

        self.assertEqual(vopn_map.get_oid('aaa.txt'), 'oid1')
        self.assertEqual(vopn_map.get_oid('bbb.txt'), 'oid2')
        self.assertEqual(vopn_map.get_vopn('oid1'), 'aaa.txt')
        self.assertEqual(vopn_map.get_vopn('oid2'), 'bbb.txt')

    def test_2(self):
        vopn_map = VOPNMap()

        vopn_map.upsert_vopn('aaa.txt', 'oid1')
        vopn_map.upsert_vopn('bbb.txt', 'oid2')
        vopn_map.upsert_vopn('aaa.txt', 'oid3')

        self.assertEqual(vopn_map.get_oid('aaa.txt'), 'oid3')
        self.assertEqual(vopn_map.get_oid('bbb.txt'), 'oid2')
        self.assertEqual(vopn_map.get_vopn('oid3'), 'aaa.txt')
        self.assertEqual(vopn_map.get_vopn('oid2'), 'bbb.txt')


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    unittest.main()
