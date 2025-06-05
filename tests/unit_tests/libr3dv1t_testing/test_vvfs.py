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

from libr3dv1t.vault.vvfs import VaultVirtualFS, VirtualFile
from libr3dv1t.errors import R3D_V1T_Error


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
class TestVOPNMap(unittest.TestCase):

    def test_1(self):
        vv_fs = VaultVirtualFS()

        vf_a = VirtualFile(pname='aaa.txt')
        vf_b = VirtualFile(pname='bbb.txt')
        vf_a2 = VirtualFile(pname='aaa222.txt')

        vv_fs.link_file(vf=vf_a, oid='oid_1')
        vv_fs.link_file(vf=vf_b, oid='oid_2')
        vv_fs.link_file(vf=vf_a2, oid='oid_1')

        self.assertEqual(vv_fs.get_oid('aaa.txt'), 'oid_1')
        self.assertEqual(vv_fs.get_oid('bbb.txt'), 'oid_2')
        self.assertEqual(vv_fs.get_oid('aaa222.txt'), 'oid_1')

        vfiles_oid_1 = vv_fs.oid_to_vf['oid_1']
        vfiles_oid_2 = vv_fs.oid_to_vf['oid_2']

        self.assertEqual(len(vfiles_oid_1), 2)
        self.assertEqual(len(vfiles_oid_2), 1)
        self.assertIn(vf_a, vfiles_oid_1)
        self.assertIn(vf_a2, vfiles_oid_1)
        self.assertIn(vf_b, vfiles_oid_2)

    def test_2(self):
        vv_fs = VaultVirtualFS()

        vv_fs.link_file(vf=VirtualFile(pname='aaa.txt'), oid='oid_1')
        vv_fs.link_file(vf=VirtualFile(pname='bbb.txt'), oid='oid_2')
        vv_fs.link_file(vf=VirtualFile(pname='aaa.txt'), oid='oid_3')

        self.assertEqual(vv_fs.get_oid('aaa.txt'), 'oid_3')
        self.assertEqual(vv_fs.get_oid('bbb.txt'), 'oid_2')
        # self.assertEqual(vv_fs.get_vf_by_oid('oid_3'), VirtualFile(pname='aaa.txt'))
        # self.assertEqual(vv_fs.get_vf_by_oid('oid_2'), VirtualFile(pname='bbb.txt'))


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    unittest.main()
