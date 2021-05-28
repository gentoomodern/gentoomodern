#!/usr/bin/env python3

import re


def get_cleaned_profile(profile):
  return re.sub(re.escape('+'), '-', profile) # Found that one out when working with musl+selinux...
