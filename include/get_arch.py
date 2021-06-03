#!/usr/bin/env python3


import os
from .gentoomuch_common import arch_config_path

def get_arch() -> str:
    return open(open_config_path, 'r').read().strip()
