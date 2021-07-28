#!/usr/bin/env python3

import os
from .gentoomodern_common import arch_config_path, output_path, desired_stage_path, desired_profile_path
from .swap_stage import swap_stage
from .composefile import create_composefile
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_desired_profile import get_desired_profile
from .get_desired_stage import get_desired_stage
from .get_gentoomodern_uid import get_gentoomodern_uid


def freshroot():
    arch = open(arch_config_path).read().strip()
    if os.path.isfile(desired_profile_path):
        desired_profile = open(desired_profile_path).read().strip()
        print("    Trying to start fresh root with profile " + desired_profile + " and stage definition ")
        swap_stage(arch, desired_profile, "gentoomodern/builder", False) 
        os.system("cd " + output_path + " && docker-compose up --no-start 2> /dev/null && docker-compose run gentoomodern-builder /bin/bash 2> /dev/null")
    else:
        print("You need to set a profile prior to starting a fresh root.")
