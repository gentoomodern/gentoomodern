#!/usr/bin/env python3

import re


def get_dockerized_stagedef(profile):
  return re.sub('/', '-', profile)
