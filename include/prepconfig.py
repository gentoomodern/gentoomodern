#!/usr/bin/env python3

import sys, os, re
from include.common import read_by_tokens, read_file_lines, write_file_lines
from typing import Dict, List, Set

msg_prefix       = '[Zentoo.prep-conf] '
config_dir      = './config/'
stage_path       = config_dir + 'stage.defines/'
cpu_path         = config_dir + 'cpu.defines/'
pkgset_path      = config_dir + 'portage.global/'
flagset_path     = config_dir + 'portage.configs/'
hooks_path       = config_dir + 'build.hooks/'
#kernel_path     = config_dir + 'kernel.defines/'

def get_flagname(flag_str):
    return re.sub('^(-)+', '', flag_str)


def get_flagname_test():
    if not get_flagname('silly-thing/dontchangeme') == 'silly-thing/dontchangeme':
        sys.exit("Failed get_flagname test: Should not change flags' contents.")
    if not get_flagname('-silly-thing/testme') == 'silly-thing/testme':
        sys.exit('Failed get_flagname test: Single neg.')
    if not get_flagname('--silly-thing/testmemore') == 'silly-thing/testmemore':
        sys.exit('Failed get_flagname test: Multiple negative signs.')
    if not get_flagname('-') == '':
        sys.exit('Failed get_flagname test: Empty flag.')

get_flagname_test()

# This deduplicates keywords and verifies for set/unset combinations.
def ingest_conf(file_content_list, variables_to_flags: Dict[str, Dict[bool, List[str]]], debug = False):
    for line in file_content_list:
        if not re.match('(\S)+', line): # Only proceed if we have an empty line... Those make the regex crash
            continue
        if debug:
            print('ZENTOO DEBUG - line: ' + line)
        line = re.sub('(=|\'|")+', ' ', line) # Strip out troublesome characters
        variable_name = re.match('^\S+', line).group()
        if variable_name[0] == '#': # Skip comments
            continue
        if debug:
            print('ZENTOO DEBUG - line (cleaned): ' + line)
            print('ZENTOO DEBUG - variable name: ' + variable_name)
        flags_str = re.sub('^' + re.escape(variable_name), '', line)
        if debug:
            print('ZENTOO DEBUG - flags string: ' + flags_str)
        if not variable_name in variables_to_flags:
            variables_to_flags[variable_name] = dict()
        
        if True not in variables_to_flags[variable_name]:
            variables_to_flags[variable_name][True] = dict()
            variables_to_flags[variable_name][True] = []
        if False not in variables_to_flags[variable_name]:
            variables_to_flags[variable_name][False] = dict()
            variables_to_flags[variable_name][False] = []

        is_setting = False
        for candidate_flag in flags_str.split():
            if not candidate_flag.strip() == '':
                if debug:
                    print('Examining flag ' + candidate_flag)
                flag_abs = get_flagname(candidate_flag)
                if flag_abs == candidate_flag:
                    is_setting = True
                else:
                    is_setting = False
                if is_setting:
                    if flag_abs in variables_to_flags[variable_name][True]:
                        continue
                    elif flag_abs in variables_to_flags[variable_name][False]:
                        return False
                    else:
                        variables_to_flags[variable_name][True].append(flag_abs)
                if not is_setting:
                    if flag_abs in variables_to_flags[variable_name][True]:
                        return False
                    elif flag_abs in variables_to_flags[variable_name][False]:
                        continue
                    else:
                        variables_to_flags[variable_name][False].append(flag_abs)
    return True


# Determine equivalence partitions.
def ingest_conf_test():
    desired = { 'AB': { True: ['nice-enough'], False: ['awful'] } }
    results = dict()
    test_1 = ['AB=\'-awful nice-enough\'', 'AB=-awful']
    if not ingest_conf(test_1, results):
        sys.exit('Failed ingest_conf: testset1. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_conf: testset1. Bad results.')
    test_2 = ['AB = -awful nice-enough -awful']
    if not ingest_conf(test_2, results):
        sys.exit('Failed ingest_conf: testset2. Should return true.')
    if not results == desired:
       sys.exit('Failed ingest_conf: testset2. Bad results.')
    test_3 = ['AB="-awful nice-enough awful"']
    if ingest_conf(test_3, results):
        sys.exit('Failed ingest_conf: testset3 (yes and no). Should return false.')
    if not results == desired:
        sys.exit('Failed ingest_conf: testset3 (yes and no). Bad results.')
    test_4 = ["AB='nice-enough -awful nice-enough'", "AB=' nice-enough'"]
    if not ingest_conf(test_4, results):
        sys.exit('Failed ingest_conf: testset4. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_conf: testset4. Bad results.')


ingest_conf_test()
