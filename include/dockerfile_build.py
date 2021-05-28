#!/usr/bin/env python3

# import os, docker
from .get_stage import get_stage
from .stage_exists import stage_exists
from .get_tarball_name import get_tarball_name
from .tarball_exists import tarball_exists
from .pull_stage import pull_stage


def stage_bootstrap(arch, profile, force_build = False):
    custom_url = 
    # Check for the stage image.
    missing = bool(not stage_exists(arch, profile, True))
    # Gotta build the stage
    if missing:
        print("INFO: stage_build: " + get_stage_name(arch, profile, bool(upstream)) + " being built.")
        pull_stage(arch, profile, custom_url, bool(upstream))
    elif force_build:
        print("INFO: stage_build: " + get_stage_name(arch, profile, bool(upstream)) + " present but force-rebuilt.")
        pull_stage(arch, profile, custom_url, bool(upstream))
    else:
        print("INFO: stage_build: " + get_stage_name(arch, profile, bool(upstream)) + " already present on system... No need to build it. Cool, huh?")
# With our arguments, we can now create the second Dockerfile, which we build and tag.
