#!/usr/bin/env python3

import docker
import os
from include.gentoomuch_common import arch_config_path, current_profile_path, profiles_amd64, output_path

def list_profiles():
  # Get currently active profile
  current = open(current_profile_path).read().strip()
  print("Listing compatible system profiles:")
  for p in profiles_amd64:
    print(('[*] ' if p == current else '[ ] ') + p)
  exit()
