#!/usr/bin/env python3

from .gentoomuch_common import desired_stage_path


def get_desired_stage():
    return ((True, open(desired_stage_path, 'r').read().strip()) if os.path.isdir(desired_stage_path) else (False, ''))
