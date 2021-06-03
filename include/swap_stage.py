#!/usr/bin/env python3

# This sets the currently active basestage.
import os, sys, re, docker
from .gentoomuch_common import output_path, config_path, image_tag_base, active_image_tag, desired_packages_path, desired_hooks_path
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_dockerized_profile_name import get_dockerized_profile_name
from .portage_directory_combiner import portage_directory_combiner
from .get_docker_tag import get_docker_tag
from .composefile import create_composefile
from .write_file_lines import write_file_lines


def swap_stage(arch, profile, stage_def, upstream : bool, exported_patch: str = ''):
    os.system('cd ' + output_path + ' && docker-compose down')
    combiner = portage_directory_combiner()
    combiner.process_stage_defines(stage_def)
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    found = False
    t = get_docker_tag(arch, profile, stage_def, bool(upstream))
    # print("ATTEMPTING TO SWAP: " + t)
    for i in dckr_imgs:
        if t in i.tags:
            os.system('docker rmi ' + active_image_tag) # To ensure we don't suffer from duplicates.
            i.tag(active_image_tag) # We now actually tag the image we wanna use.
            found = True
            print('SWAPPED STAGE TO: ' + t)
            break
    if not found:
        sys.exit("FAILED TO SWAP STAGE: Could not find docker image " + t)
    if 'packages' in combiner.todo:
        if len(combiner.todo['packages']) > 0:
            write_file_lines(desired_packages_path, combiner.todo['packages'])
    if 'hooks' in combiner.todo:
        if len(combiner.todo['hooks']) > 0:
            write_file_lines(desired_hooks_path, combiner.todo['hooks'])
    create_composefile(output_path, exported_patch)
    os.system('cd ' + output_path + ' && docker-compose up --no-start')
