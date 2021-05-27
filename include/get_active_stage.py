#!/usr/bin/env python3

import re, docker
from .gentoomuch_common import image_tag_base, active_image_tag, profiles_amd64_cleaned
from .tag_parser import tag_parser

def get_active_stage():
    dckr = docker.from_env()
    for i in dckr.images.list():
        if active_image_tag in i.tags:
            cleaned_tags = i.tags
            cleaned_tags.remove(active_image_tag)
            if len(cleaned_tags) > 1:
                exit("Multiple active stages defined. This is an error")
            for t in cleaned_tags:
                print('GOT ACTIVE STAGE: ' + t)
                parser = tag_parser()
                parser.parse(t)
                return parser
    exit("No active stage defined!")
