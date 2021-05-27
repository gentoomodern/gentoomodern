#!/usr/bin/env python3

import os
from .gentoomuch_common import arch_config_path, output_path, desired_stage_path, desired_profile_path, get_cleaned_profile, get_cleaned_stagedef
#from .get_active_stage import get_active_stage, tag_parser
from .swap_stage import swap_stage

def freshroot():
    arch = open(arch_config_path).read().strip()
    if os.path.isfile(desired_profile_path) and os.path.isfile(desired_stage_path):
        desired_profile = open(desired_profile_path).read().strip()
        desired_stage = open(desired_stage_path).read().strip()
        print("    Trying to start fresh root with profile " + desired_profile + " and stage definition " + desired_stage) 
        swap_stage(arch, desired_profile, desired_stage) 
        os.chdir(output_path)
        os.system("docker-compose up --no-start && docker-compose run gentoomuch-builder /bin/bash")
    else:
        if not os.path.isfile(desired_profile_path) and not os.path.isfile(desired_stage_path):
            print("User-defined profile and stage defines unset.")
        elif not os.path.isfile(desired_profile_path):
            print("Profile path not set.")
        else:
            print("Stage path not set.")         
