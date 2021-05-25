#!/usr/bin/env python3

# This sets the currently active basestage.
import os, sys, re, docker
from include.gentoomuch_common import config_path, read_file_lines, write_file_lines, image_tag_base, active_image_tag
from include.portage_directory_combiner import portage_directory_combiner

def swap_stage(arch, profile, stage_define, upstream = False):
    os.system('docker rmi ' + active_image_tag) # To ensure we don't suffer from duplicates.
    cleaned_profile = re.sub(re.escape('+'), '-', profile) # Found that one out when working with musl+selinux...
    cleaned_stage_define = re.sub('/', '-', stage_define) # / gets intepreted as a repository in docker, so fix that up.
    combiner = portage_directory_combiner()
    combiner.process_stage_defines(stage_define)
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    if upstream:
        tag_tail = arch + '-' + cleaned_profile + ':upstream' # We use the upstream stage3.
    else:
        tag_tail = arch + '-' + cleaned_profile + '-' + cleaned_stage_define + ':local' # We use the locally-built stage3.
    t = image_tag_base + tag_tail
    did_something = False
    for i in dckr_imgs:
        if t in i.tags:
            print('GOTCHA: ' + t)
            i.tag(active_image_tag) # We now actually tag the image we wanna use.
            did_something = True
            break
    if not did_something:
        sys.exit("Could not find docker image " + t)
