#!/usr/bin/env python3

import os, docker
from .gentoomuch_common import desired_profile_path, profiles_amd64
from .docker_stage_exists import docker_stage_exists


def set_desired_profile(arch, profile):
    if profile not in profiles_amd64 or not (docker_stage_exists(arch, profile, 'gentoomuch/builder', False) or docker_stage_exists(arch, profile, '', True)):
        exit("Profile not bootstrapped yet.")
    print("Setting Gentoomuch profile to " + profile)
    if os.path.isfile(desired_profile_path):
        os.remove(desired_profile_path)
    open(desired_profile_path, 'w').write(profile)
