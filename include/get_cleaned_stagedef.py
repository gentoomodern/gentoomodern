#!/usr/bin/env python3

import re


def get_cleaned_stagedef(profile):
  return re.sub('/', '-', profile)
