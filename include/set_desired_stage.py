#!/usr/bin/env python3

import os
from .gentoomuch_common import desired_stage_path

def set_desired_stage(stagedef):
    if os.path.isfile(desired_stage_path):
        os.remove(desired_stage_path)
    open(desired_stage_path, 'w').write(stagedef)
