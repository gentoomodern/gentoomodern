#!/usr/bin/env python3

import docker
import os
from include.gentoomuch_common import arch_config_path, desired_profile_path, profiles_amd64, output_path
from .docker_stage_exists import docker_stage_exists

def list_profiles(arch):
    no_profile = False
    # Get currently active profile
    if os.path.isfile(desired_profile_path):
        desired = open(desired_profile_path).read().strip()
    print("Listing compatible system profiles:")
    ctr = 1
    for p in profiles_amd64:
        if docker_stage_exists(arch, p, 'gentoomuch/builder', False):
            bootstrapped_indicator = ' [B] '
        else:
            bootstrapped_indicator = ' [ ] '

        print(bootstrapped_indicator +(' [*] ' if p == desired else ' [ ] ') + str(ctr) + ' ' + p)
        ctr += 1
    exit()
