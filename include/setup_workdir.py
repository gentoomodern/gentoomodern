#!/usr/bin/env python3

import os
from .gentoomuch_common import emergelogs_path, profiles_amd64_dockerized


def setup_workdir(arch):
    if arch  == 'amd64':
        for p in profiles_amd64_dockerized:
            os.makedirs(os.path.join(emergelogs_path, p), exist_ok = True)
    else:
        print("Could not create stage paths.")
