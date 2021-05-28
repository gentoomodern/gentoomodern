#!/usr/bin/env python3

import os
from .gentoomuch_common import stages_path
from .get_tarball_name import get_tarball_name


def tarball_exists(arch, profile, stage_define, upstream = False):
    # Get tarball name. Check path.
    return os.path.isfile(os.path.join(stages_path, get_tarball_name(arch, profile, stage_define, bool(upstream))))
