#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import stage_defines_path, desired_stage_path

# This lists stages
def list_stages():
  # Get currently active stage. Indexing by number is not allowed in this tool: indexing would break once a new stage gets defined, leading to user surprises. :(.
  if not os.path.isfile(desired_stage_path):
    exit('No current stage path config file found at ' + desired_stage_path)
  current = open(desired_stage_path).read().strip()
  print("Listing user-defined stages:")
  for dirpath, dirs, files in sorted(os.walk(stage_defines_path)):
    if not dirs:
      d = re.sub(stage_defines_path, '', dirpath)
      print(('[*] ' if d == current else '[ ] ') + ' ' + d)
