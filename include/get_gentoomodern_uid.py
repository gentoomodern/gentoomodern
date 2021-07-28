#!/usr/bin/env python3

import os
from .gentoomodern_common import config_env_path

def get_gentoomodern_uid() -> str:
    return open(os.path.join(config_env_path, 'uid'), 'r').read().strip()
