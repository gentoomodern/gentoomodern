#!/usr/bin/env python3

import os
from .get_active_stage import get_active_stage, tag_parser

def freshroot():
    os.chdir('work')
    stage = get_active_stage()
    os.system("docker-compose up --no-start && docker-compose run gentoomuch-builder")
