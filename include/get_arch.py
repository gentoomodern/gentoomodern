#!/usr/bin/env python3


import os
from .gentoomodern_common import env_settings_path

def get_arch() -> str:
    return open(os.path.join(env_settings_path, 'arch'), 'r').read().strip()
