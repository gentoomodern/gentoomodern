#!/usr/bin/env python3

# This sets the currently active basestage.
import os, sys, re, docker
from .gentoomuch_common import output_path, config_path, image_tag_base, active_image_tag, desired_packages_path, desired_hooks_path, get_cleaned_stagedef, get_cleaned_profile
from .portage_directory_combiner import portage_directory_combiner
from .get_docker_tag import get_docker_tag
from .composefile import create_composefile

def swap_stage(arch, profile, stage_def, upstream = False):
    os.system('cd ' + output_path + ' && docker-compose down')
    combiner = portage_directory_combiner()
    combiner.process_stage_defines(stage_def)
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    did_something = False
    t = get_docker_tag(arch, profile, stage_def, bool(upstream))
    print("ATTEMPTING TO SWAP: " + t)
    for i in dckr_imgs:
        if t in i.tags:
            os.system('docker rmi ' + active_image_tag) # To ensure we don't suffer from duplicates.
            i.tag(active_image_tag) # We now actually tag the image we wanna use.
            did_something = True
            print('SWAPPED STAGE TO: ' + t)
            break
    if not did_something:
        sys.exit("FAILED TO SWAP STAGE: Could not find docker image " + t)
    if 'packages' in combiner.todo:
        if len(combiner.todo['packages']) > 1:
            write_file_lines(combiner.todo['packages'], desired_package_path)
    if 'hooks' in combiner.todo:
        if len(combiner.todo['hooks']) > 1:
            write_file_lines(combiner.todo['hooks'], desired_hooks_path)
    create_composefile(output_path)
    os.system('cd ' + output_path + ' && docker-compose down && docker-compose up --no-start')
