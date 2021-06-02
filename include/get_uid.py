#!/usr/bin/env python3

import os
from .gentoomuch_common import env_settings_path

def get_uid() -> str:
    path = os.path.join(env_settings_path, 'uid')
