#!/usr/bin/env python3

import os

def prep_config():
    return os.system('rsync -aXHp ./config ./build')
