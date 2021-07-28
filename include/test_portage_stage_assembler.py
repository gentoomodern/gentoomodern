#!/usr/bin/env python3

import os, unittest
from .gentoomodern_common import global_portage_config_path, cpu_defines_path
from .portage_stage_assembler import portage_stage_assembler
from .portage_file_munger import 

#############################################################################
# How we gonna do this thing???                                             #
#############################################################################
# 1. Get a line-by-line of desired outputs.                                 #
# FOR EACH CONFIG:                                                          #
#   2. Amend the common data to reflect new test case                       #
#   3. Clean up the output directory                                        #
#   4. Run our stage assembler over the test data.                          #
#   5. Verify presence of all required files in output dir.                 #
#   6. Verify presence of all relevant lines in the output files.           #
#   7. Verify absence of any excess data.                                   #
#############################################################################

baseline_files = {}
baseline_files['make.conf'] = read_file_lines(os.path.join(cpu_defines_path, 'gentoomodern/test'))
baseline_files['make.conf'].extend(read_file_lines(os.path.join(global_portage_config_path, 'make.conf')))
baseline_files['package.accept_keywords'] = read_file_lines(os.path.join(global_portage_config_path, 'package.accept_keywords'))
baseline_files['repos.conf/gentoo.conf'] = read_file_lines(os.path.path(global_portage_config_path, 'repos.conf/gentoo.conf'))


class test_portage_stage_assembler(unittest.TestCase):

    def setUp(self):
        # 1.
        var = 0

    def tearDown(self):
        var = 0


    # This'll be the test for our most basic, functional form of configuration.
    def test_basecase(self):
        var = 0
        # 2. N/A
        # 3.
        # 4.
        # 5.
        # 6.
        # 7.
        self.assertTrue(var == 0)

    # We apply a patch to our profile.
    def test_patching_basecase(self):
        var = 0
    #################################################################################################################################
    # We try to apply two patches to our profile, and they're for the same package! Oh no!                                          #
    # At this stage we're really trying to avoid the inner platform antipattern, so we don't support support sequential patching    #
    # If you want to do something fancy, use ebuilds and a custom repo.                                                             #
    # This may change as we add new features to make life more scriptable.                                                          #
    #################################################################################################################################
    def test_patching_misuse(self):





if __name__ == '__main__':
    unittest.main() 
