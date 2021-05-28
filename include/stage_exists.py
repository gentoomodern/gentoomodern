#!/usr/bin/env python3

import docker
from .get_docker_tag import get_docker_tag


def stage_exists(arch, profile, stage_def, upstream = False):
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    t = get_docker_tag(arch, profile, stage_def, bool(upstream))
    for i in dckr_imgs:
        if t in i.tags:
            return True
    if not found:
        return False
