#!/usr/bin/env python3

import os
from .gentoomuch_common import desired_stage_path, config_path, stage_defines_path

def set_stage(arg):
    if os.path.isdir(os.path.join(stage_defines_path, arg)):
        print("Setting stage to " + arg)
        open(desired_stage_path, 'w').write(arg.strip())
    else:
        exit("Stage path " + arg + " does not exist")