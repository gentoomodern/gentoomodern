#!/usr/bin/env python3

import docker
import os
from include.gentoomuch_common import arch_config_path, desired_profile_path, profiles_amd64, output_path

def list_profiles():
  no_profile = False
  # Get currently active profile
  if os.path.isfile(desired_profile_path):
    current = open(desired_profile_path).read().strip()
  else:
    no_profile = True
  print("Listing compatible system profiles:")
  ctr = 1
  for p in profiles_amd64:
    if no_profile:
      print(' [ ] ' + str(ctr) + ' ' +  p)
    else:
      print((' [*] ' if p == current else ' [ ] ') + str(ctr) + ' ' + p)
    ctr += 1
  exit()
