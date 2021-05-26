#!/usr/bin/env python3

from .gentoomuch_common import current_stage_path, config_path, stage_defines_path

def set_stage(arg):
    if os.path.ispath(os.path.join(stage_defines_path, arg)):
        print("Setting stage to " + arg)
        open(current_stage_path, 'w').write(arg)
    else:
        exit("Stage path " + arg + " does not exist")
    
