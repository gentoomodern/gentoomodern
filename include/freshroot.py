#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path
from .get_active_stage import get_active_stage, tag_parser


def freshroot():
  os.chdir(output_path)
  stage = get_active_stage()
  os.system("docker-compose up --no-start && docker-compose run gentoomuch-builder /bin/bash")
