#!/usr/bin/env python3

import os
from .gentoomodern_common import env_settings_path

def get_gentoomodern_uid() -> str:
    return open(os.path.join(env_settings_path, 'uid'), 'r').read().strip()
