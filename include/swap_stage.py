#!/usr/bin/env python3

# This sets the currently active basestage.
import os, sys, re, docker
from include.gentoomuch_common import output_path, config_path, image_tag_base, active_image_tag, desired_packages_path, desired_hooks_path, get_cleaned_stage, get_cleaned_profile
from include.portage_directory_combiner import portage_directory_combiner
from include.get_docker_tag import get_docker_tag

def swap_stage(arch, profile, stage_def, upstream = False):
  os.system('cd ' + output_path + ' && docker-compose down')
  combiner = portage_directory_combiner()
  combiner.process_stage_defines(stage_def)
  dckr = docker.from_env()
  dckr_imgs = dckr.images.list()
  did_something = False
  t = get_docker_tag(arch, profile, stage_def, upstream)
  for i in dckr_imgs:
    if t in i.tags:
      print('SWAPPING STAGE: ' + t)
      os.system('docker rmi ' + active_image_tag) # To ensure we don't suffer from duplicates.
      i.tag(active_image_tag) # We now actually tag the image we wanna use.
      did_something = True
      break
    if not did_something:
      sys.exit("Could not find docker image " + t)
  if 'packages' in combiner.todo:
    if len(combiner.todo['packages']) > 1:
      write_file_lines(combiner.todo['packages'], desired_package_path)
  if 'hooks' in combiner.todo:
    if len(combiner.todo['hooks']) > 1:
      write_file_lines(combiner.todo['hooks'], desired_hooks_path)
  os.system('cd ' + output_path + ' && docker-compose up --no-start')
