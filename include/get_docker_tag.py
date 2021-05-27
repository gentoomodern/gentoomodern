#!/usr/bin/env python3
import docker
import re
from .gentoomuch_common import image_tag_base, get_cleaned_profile, get_cleaned_stagedef


def get_docker_tag(arch, profile, stage_define, upstream = False):
    cleaned_profile = get_cleaned_profile(profile) # Found that one out when working with musl+selinux...
    cleaned_stage_define = get_cleaned_stagedef(stage_define) # / gets interpreted as a repository in docker, so fix that up.
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    tag_tail = ''
    print("DEBUG: get_docker_tag: upstream = " + str(upstream))
    if upstream == True:
        tag_tail = arch + '-' + cleaned_profile + ':upstream' # We use the upstream stage3.
    else:
        tag_tail = arch + '-' + cleaned_profile + '-' + cleaned_stage_define + ':latest' # We use the locally-built stage3.
    return image_tag_base + tag_tail

