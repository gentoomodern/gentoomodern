#!/usr/bin/env python3

import os, docker
from .gentoomuch_common import desired_profile_path, profiles_amd64
from .stage_exists import stage_exists


def set_desired_profile(arch, profile):
    if profile not in profiles_amd64 or not (stage_exists(arch, profile, 'gentoomuch/builder', False) or stage_exists(arch, profile, '', True)):
        exit("Profile not bootstrapped yet.")
    print("Setting Gentoomuch profile to " + profile)
    if os.path.isfile(desired_profile_path):
        os.remove(desired_profile_path)
    open(desired_profile_path, 'w').write(profile)
