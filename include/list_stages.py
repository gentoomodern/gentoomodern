#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import stage_defines_path, current_stage_path

def list_stages():
 # Get currently active stage
  current = open(current_stage_path).read().strip()
  print("Listing user-defined stages:")
  for dirpath, dirs, files in os.walk(stage_defines_path):
    if not dirs:
      d = re.sub(stage_defines_path, '', dirpath)
      print(('[*] ' if d == current  else '[ ] ') + d)
  exit()
