#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import stage_defines_path, current_stage_path

def list_stages():
  # Get currently active stage
  if not os.path.isfile(current_stage_path):
    exit('No stage path config file found at ' + current_stage_path)
  current = open(current_stage_path).read().strip()
  print("Listing user-defined stages:")
  ctr = 1
  for dirpath, dirs, files in os.walk(stage_defines_path):
    if not dirs:
      d = re.sub(stage_defines_path, '', dirpath)
      print(('[*] ' if d == current else '[ ] ') + str(ctr) + ' ' + d)
      ctr += 1
  exit()
