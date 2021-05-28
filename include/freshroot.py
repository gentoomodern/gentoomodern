#!/usr/bin/env python3

import os
from .gentoomuch_common import arch_config_path, output_path, desired_stage_path, desired_profile_path
#from .get_active_stage import get_active_stage, tag_parser
from .swap_stage import swap_stage
from .composefile import create_composefile
from .get_cleaned_profile import get_cleaned_profile
from .get_cleaned_stagedef import get_cleaned_stagedef
def freshroot():
    arch = open(arch_config_path).read().strip()
    if os.path.isfile(desired_profile_path) and os.path.isfile(desired_stage_path):
        desired_profile = open(desired_profile_path).read().strip()
        desired_stage = open(desired_stage_path).read().strip()
        print("    Trying to start fresh root with profile " + desired_profile + " and stage definition " + desired_stage)
        create_composefile(output_path)
        swap_stage(arch, desired_profile, desired_stage) 
        os.chdir(output_path)
        os.system("docker-compose up --no-start && docker-compose run gentoomuch-builder /bin/bash")
    else:
        if not os.path.isfile(desired_profile_path) and not os.path.isfile(desired_stage_path):
            print("You need to set both a profile and stage define prior to starting a fresh root.")
        elif not os.path.isfile(desired_profile_path):
            print("You need to set a profile!")
        else:
            print("You need to set a stage define!")         
