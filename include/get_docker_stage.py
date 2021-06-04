#!/usr/bin/env python3

import docker
from .get_docker_tag import get_docker_tag


def get_docker_stage(arch: str, profile: str, stagedef:str, upstream: bool) -> (bool, str):
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    t = get_docker_tag(arch, profile, stage_def, bool(upstream))
    for i in dckr_imgs:
        if t in i.tags:
            return (True, t)
    return (False, None) 
