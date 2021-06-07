#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path, squashed_path
from .get_gentoomuch_uid import get_gentoomuch_uid

def sync():
    ##########################################################
    # Attempt to load default upstream stage (for stability) #
    ##########################################################
    if stage_exists(arch, 'default', '', True):
        swap_stage(arch, 'default', '', True)
    else:
        if download_tarball(arch, 'default'):
            swap_stage(arch, 'default', '', True)
        else:
            exit("Could not synchronize Gentoo: Dockerized stage unavailable")
    #######################################
    # Local variables for simplification. #
    #######################################
    base_path = '/mnt/squashed-portage'
    uid = get_gentoomuch_uid()
    portage_file = base_path + 'portage.squash'
    backup_file = portage_file + '.backup'
    chown_str = 'chown ' + uid + ":" + uid + " " + portage_file + " && "
    chown_str = 'chown ' + uid + ":" + uid + " " + backup_file + " "
    #####################
    # Run the commands. #
    #####################
    code = os.system("cd " + output_path + " && docker-compose run gentoomuch-updater /bin/bash -c 'mv " + portage_file + " " + backup_file + " && emerge -v --sync && emerge squashfs-tools && mksquashfs /var/db/repos/gentoo " + portage_file + " -noappend -force-gid portage -force-uid portage && " + chown_str + " && rm " + backup_file  + "'")
    #############################################################
    # Upon failure, replace the old squashed file from backup.  #
    #############################################################
    if code != 0:
        portage_file = base_path + 'portage.squash' 
        backup_file = portage_file + '.backup'
        os.system("mv " + backup_file + " " + portage_file
    #######################################################
    # Call the mounter/remounter? Or should that be done in the previous image?:tab
    
