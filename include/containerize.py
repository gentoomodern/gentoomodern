#!/usr/bin/env python3

import os, shutil
from .gentoomuch_common import output_path, stages_path, image_tag_base
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_docker_tag import get_docker_tag
from .docker_stage_exists import docker_stage_exists
from .bootstrap_dockerfile import bootstrap_dockerfile


# This turns a tarball into a dockerized stage
def containerize(tarball_name, arch, profile, stagedef, upstream: bool) -> bool:
    print("Called containerize. Taball name " + tarball_name + " profile = " + profile + ", stagedef = " + stagedef + " upstream " + str(upstream))
    # This tag is used to name an image that is imported as a bootstrap image.
    bootstrap_tag = image_tag_base + "bootstrap:latest"
    desired_tag = get_docker_tag(arch, profile, stagedef, bool(upstream))
    print("Containerize... desired tag = " + desired_tag)
    # Which directory do we use to build?
    # If it exists, we're doing an update and thus we remove. TODO: Replace with renaming and allow recovery from failed backup.
    if docker_stage_exists(arch, profile, stagedef, bool(upstream)):
        os.system("docker image rm -f " + desired_tag)
    bootstrap_dir = os.path.join(output_path, 'bootstrap')
    dockerfile = os.path.join(bootstrap_dir, 'Dockerfile')
    os.makedirs(bootstrap_dir, exist_ok = True)
    if len(os.listdir(bootstrap_dir)) > 0:
        os.system('rm -rf ' + bootstrap_dir + '/*')
    # Delete the dockerfile, if present from another build...
    if os.path.isfile(dockerfile):
        os.remove(dockerfile)
    old_tarball_path = os.path.join(stages_path, tarball_name)
    new_tarball_path = os.path.join(bootstrap_dir, tarball_name) 
    # Now create our dockerfile.
    open(dockerfile, 'w').write(bootstrap_dockerfile(tarball_name, profile))
    shutil.move(old_tarball_path, new_tarball_path)
    # We then import our bootstrap image, then build a new one using our dockerfile. Then we get rid of the old bootstrap image.
    code = os.system("cd " + bootstrap_dir + " && docker import " + tarball_name  + " " + bootstrap_tag + " && docker build -t " + desired_tag + " . && docker image rm -f " + bootstrap_tag + " &> /dev/null")
    shutil.move(new_tarball_path, old_tarball_path)
    if code == 0:
        print("INFO: Succesfully dockerized " + desired_tag)
        return True
    else:
        return False
