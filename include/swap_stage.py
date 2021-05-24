#!/usr/bin/env python3

# This sets the currently active basestage.
import os, sys, re, docker
from include.gentoomuch_common import config_path, read_file_lines, write_file_lines, image_tag_base
from include.portage_directory_combiner import portage_directory_combiner

def swap_stage(arch, profile, stage_define, upstream = False):
    cleaned_stage_define = re.sub('/', '-', stage_define)
    cleaned_profile = re.sub(re.escape('+'), '-', profile)
    combiner = portage_directory_combiner()
    combiner.process_stage_defines(stage_define)
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    if upstream:
        tag_tail = arch + '-' + cleaned_profile + ':upstream'
    else:
        tag_tail = arch + '-' + cleaned_profile + '-' + cleaned_stage_define + ':local'
    t = image_tag_base + tag_tail
    did_something = False
    for i in dckr_imgs:
        if t in i.tags:
            print('GOTCHA')
            i.tag(image_tag_base + 'current' , 'latest')
            did_something = True
            break
    if not did_something:
        sys.exit("Could not find docker image " + t)
