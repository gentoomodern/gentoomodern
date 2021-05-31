#!/usr/bin/env python3

import os
from .gentoomuch_common import upstream_stages_path, local_stages_path, image_tag_base
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_docker_tag import get_docker_tag
from .docker_stage_exists import docker_stage_exists
from .bootstrap_dockerfile import bootstrap_dockerfile


# This turns an already-present tarball and turns it into a stage
def containerize(tarball_name, arch, profile, stagedef, upstream):
    bootstrap_tag = image_tag_base + "bootstrap:latest"
    dir_name = upstream_stages_path if upstream else local_stages_path 
    if docker_stage_exists(arch, profile, stagedef, bool(upstream)):
        os.system("docker image rm -f " + get_docker_tag(arch, profile, stagedef, bool(upstream)))
    if os.path.isfile(os.path.join(dir_name, 'Dockerfile')):
        os.remove(os.path.join(dir_name, 'Dockerfile'))
    open(os.path.join(dir_name, 'Dockerfile'), 'w').write(bootstrap_dockerfile(tarball_name))
    os.system("cd " + dir_name + " && docker image rm -f " + bootstrap_tag + " &> /dev/null")
    os.system("cd " + dir_name + " && docker import " + tarball_name  + " " + bootstrap_tag + " && docker build --no-cache . -t " + get_docker_tag(arch, profile, stagedef, bool(upstream)) + " && docker image rm -f " + bootstrap_tag + " &> /dev/null")
    print("INFO: Succesfully dockerized " + get_docker_tag(arch, profile, stagedef, bool(upstream)))
    return True
