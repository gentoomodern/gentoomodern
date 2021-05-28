#!/usr/bin/env python3

import os
from .gentoomuch_common import desired_packages_path, output_path
from .read_file_lines import read_file_lines


def run_build(empty_tree : False):
  packages = []
  if os.path.isdir(desired_packages_path):
    packages = read_file_lines(desired_packages_path)
  pkgs_str = ''
  if len(packages) > 0:
    needs_to_install_more_stuff = True
    for p in packages:
      pkgs_str += p.strip()
      pkgs_str +=  ' '
  cmd_str = "cd " + output_path + " && docker-compose run gentoomuch-builder /bin/bash -c 'emerge -uDqv " + ("--emptytree" if empty_tree else "--changed-use")  + ' ' + pkgs_str + "@world'"
  code = os.system(cmd_str)
  if code != 0:
    exit("Issues while compiling!")
