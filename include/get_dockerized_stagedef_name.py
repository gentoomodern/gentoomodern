#!/usr/bin/env python3

import re


def get_dockerized_stagedef_name(profile):
  return re.sub('/', '-', profile)
