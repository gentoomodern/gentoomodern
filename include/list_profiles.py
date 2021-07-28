#!/usr/bin/env python3

import os, docker
from include.gentoomodern_common import desired_profile_path, profiles_amd64, output_path
from .stage_exists import stage_exists
from .get_desired_profile import get_desired_profile


def list_profiles(arch):
    desired_profile_info = get_desired_profile()
    if desired_profile_info[0]:
        desired = desired_profile_info[1]
        has_desired_profile = True
    else:
        has_desired_profile = False
    print("Listing compatible system profiles:")
    for p in profiles_amd64:
        if stage_exists(arch, p, 'gentoomodern/builder', False):
            bootstrapped_indicator = 'GOOD TO GO :)  '
        elif stage_exists(arch, p, '', True):
            bootstrapped_indicator = 'UPSTREAM READY '
        else:
            bootstrapped_indicator = 'NOT INSTALLED  '
        if has_desired_profile and p == desired:
            desired_indicator = '[*]'
        else:
            desired_indicator = '[ ]'
        print(' ' + bootstrapped_indicator + ' ' + desired_indicator + '       ' + p)
    exit()
