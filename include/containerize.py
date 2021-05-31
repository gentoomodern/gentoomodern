#!/usr/bin/env python3

import os
from .gentoomuch_common import stages_path, image_tag_base
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
    # Delete the dockerfile, if present from another build...
    if os.path.isfile(os.path.join(stages_path, 'Dockerfile')):
        os.remove(os.path.join(stages_path, 'Dockerfile'))
    # Now create our dockerfile.
    open(os.path.join(stages_path, 'Dockerfile'), 'w').write(bootstrap_dockerfile(tarball_name))
    
    # We then import our bootstrap image, then build a new one using our dockerfile. Then we get rid of the old bootstrap image.
    code = os.system("cd " + stages_path + " && docker import " + tarball_name  + " " + bootstrap_tag + " && docker build -t " + desired_tag + " . && docker image rm -f " + bootstrap_tag + " &> /dev/null")
    if code == 0:
        print("INFO: Succesfully dockerized " + desired_tag)
        return True
    else:
        return False
