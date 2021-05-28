#!/usr/bin/env python3

import os
from .gentoomuch_common import stages_path
from .get_cleaned_profile import get_cleaned_profile
from .get_cleaned_stagedef import get_cleaned_stagedef
from .get_docker_tag import get_docker_tag
from .tarball_exists import tarball_exists
from .stage_exists import stage_exists

# This turns an already-present tarball and turns it into a stage
def containerize(arch, profile, stagedef, upstream = False):
    if not tarball_exists(arch, profile, stagedef, bool(upstream)):
        download_tarball(arch, profile, stagedef, bool(upstream))
    # Check path, then ingest if good.
    if stage_exists(arch, profile, stagedef, bool(upstream)):
        os.system("cd " + stage_path + " docker rmi " + get_docker_tag(arch, profile, stagedef, bool(upstream)))
