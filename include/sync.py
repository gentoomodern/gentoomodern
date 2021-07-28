#!/usr/bin/env python3

import os
from .gentoomodern_common import output_path, squashed_path
from .get_gentoomodern_uid import get_gentoomodern_uid
from .stage_exists import stage_exists
from .swap_stage import swap_stage

def sync(arch):
    ##########################################################
    # Attempt to load default upstream stage (for stability) #
    ##########################################################
    if stage_exists(arch, 'default', 'gentoomodern/builder', True):
        swap_stage(arch, 'default', 'gentoomodern/builder', True)
    else:
        if download_tarball(arch, 'default'):
            swap_stage(arch, 'default', 'gentoomodern/builder', True)
        else:
            exit("Could not synchronize Gentoo: Dockerized stage unavailable")
    print("*********************************************************")
    print("*** Synchronizing with upstream Portage repository... ***")
    print("*********************************************************")
    code = os.system("cd " + output_path + " && docker-compose run gentoomodern-updater /bin/bash -c 'emerge --sync'")
