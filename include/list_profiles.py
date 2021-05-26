#!/usr/bin/env python3

import docker
import os
from include.gentoomuch_common import arch_config_path, current_profile_path, profiles_amd64, output_path

def list_profiles():
  # Get currently active profile
  if not os.path.isfile(current_profile_path):
    exit('No profile path config file found at ' + current_profile_path)
  current = open(current_profile_path).read().strip()
  print("Listing compatible system profiles:")
  ctr = 1
  for p in profiles_amd64:
    print(('[*] ' if p == current else '[ ] ') + str(ctr) + ' ' + p)
    ctr += 1
  exit()
