#!/usr/bin/env python3

import re, docker
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name


def get_tarball_name(arch, profile, stage_define, upstream = False, ext = 'xz'):
    base = 'stage3'
    tail = ''
    # We use the upstream stage3.
    if upstream == True:
        tail = arch + '-' + profile
    # We use the locally-built stage3.
    else:
        tail = arch + '-' + profile + '-' + get_dockerized_stagedef(stage_define)
    tail += '.tar.' + ext
    return base + tail

