#!/usr/bin/env python3

import docker
from .gentoomodern_common import active_image_tag
from .tag_parser import tag_parser


def get_active_stage():
    dckr = docker.from_env()
    for i in dckr.images.list():
        if active_image_tag in i.tags:
            cleaned_tags = i.tags
            cleaned_tags.remove(active_image_tag)
            if len(cleaned_tags) > 1:
                exit("ERROR: MULTIPLE ACTIVE STAGES DEFINED.")
            for t in cleaned_tags:
                print('INFO: GOT ACTIVE STAGE: ' + t)
                parser = tag_parser()
                parser.parse(t)
                return parser
    exit("ERROR: NO ACTIVE STAGE DEFINED IN DOCKER ENVIRONMENT.")
