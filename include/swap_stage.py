#!/usr/bin/env python3
# This sets the currently active basestage.
import os, sys, docker
from include.gentoomuch_common import config_path, read_file_lines, write_file_lines
from include.portage_directory_combiner import portage_directory_combiner, image_tag_base

def swap_stage(arch, profile, stage_definition, upstream = False):
    cleaned_profile = re.sub(re.escape('+'), '-', profile)
    combiner = portage_directory_combiner()
    combiner.process_stage_defines(stage_definitions)
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    if upstream:
        tag_tail = arch + '-' + cleaned_profile + ':upstream'
    else:
        tag_tail = arch + '-' + cleaned_profile + '-' + stage_definition + ':local'
    t = image_tag_base + tag_tail
    did_something = False
    for i in dckr_imgs:
        if t in i.tags:
            print('GOTCHA')
            i.tag(image_tag_base + 'current' , 'latest')
            did_something = True
            break
    return did_something
