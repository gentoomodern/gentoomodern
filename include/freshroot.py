#!/usr/bin/env python3

import os
from .gentoomuch_common import arch_config_path, output_path, desired_stage_path, desired_profile_path
from .swap_stage import swap_stage
from .composefile import create_composefile
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_desired_profile import get_desired_profile
from .get_desired_stage import get_desired_stage
from .get_gentoomuch_uid import get_gentoomuch_uid

def freshroot():
    arch = open(arch_config_path).read().strip()
    if os.path.isfile(desired_profile_path) and os.path.isfile(desired_stage_path):
        desired_profile = open(desired_profile_path).read().strip()
        desired_stage = open(desired_stage_path).read().strip()
        print("    Trying to start fresh root with profile " + desired_profile + " and stage definition " + desired_stage)
        create_composefile(output_path)
        swap_stage(arch, desired_profile, desired_stage, False) 
        os.system("cd " + output_path + " && docker-compose up --no-start && docker-compose run gentoomuch-builder /bin/bash")
    else:
        if not os.path.isfile(desired_profile_path) and not os.path.isfile(desired_stage_path):
            print("You need to set both a profile and stage define prior to starting a fresh root.")
        elif not os.path.isfile(desired_profile_path):
            print("You need to set a profile!")
        else:
            print("You need to set a stage define!")         
