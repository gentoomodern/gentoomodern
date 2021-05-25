#!/usr/bin/env python3

import os

def sync(force = False):
    squashed_path = '/mnt/squashed-portage/portage.squash'
    uid = open(uid_config_path).read().strip()
    has_gid = False
    if os.path.isfile(gid_config_path).read().strip():
        has_gid = True
        gid = open(gid_config_path).read().strip()
    os.system("cd work && docker-compose up && docker-compose run gentoomuch-updater /bin/bash -c '" + ("rm " + squashed_path + " && " if force else "") + "emerge --sync && emerge squashfs-tools && mksquashfs /var/db/repos/gentoo " + squashed_path + " -noappend -force-gid portage -force-uid portage && chown " + str(uid) + ":" + (str(gid) if has_gid else str(uid)) + squashed_path + "'")
