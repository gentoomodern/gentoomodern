#!/usr/bin/env python3

from .gentoomuch_common import desired_profile_path, profiles_amd64

def set_desired_profile(arg):
  if arg in profiles_amd64:
    print("Setting profile to " + arg)
    open(desired_profile_path, 'w').write(arg)
  else:
    exit("Invalid profile name: " + arg)
