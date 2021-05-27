#!/usr/bin/env python3

import docker
import re
from .gentoomuch_common import get_cleaned_profile, get_cleaned_stagedef

def get_tarball_name(arch, profile, stage_define, upstream = False):
    base = 'stage3'
    tail = ''
    # We use the upstream stage3.
    if upstream == True:
        tail = '-upstream-' + arch + '-' + get_cleaned_profile(profile)
    # We use the locally-built stage3.
    else:
        tail = arch + '-' + get_cleaned_profile(profile) + '-' + get_cleaned_stagedef(stage_define)
    tail += '.tar.xz'
    return base + tail

