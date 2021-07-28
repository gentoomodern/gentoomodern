#!/usr/bin/env python3


import os
from .gentoomodern_common import config_arch_path

def get_arch() -> str:
    return open(config_arch_path, 'r').read().strip()
