#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path
from .get_gentoomuch_uid import get_gentoomuch_uid

def sync():
    squashed_path = '/mnt/squashed-portage/portage.squash'
    os.system("cd " + output_path + " && docker-compose run gentoomuch-updater /bin/bash -c 'rm " + squashed_path + " & emerge --sync && emerge squashfs-tools && mksquashfs /var/db/repos/gentoo " + squashed_path + " -noappend -force-gid portage -force-uid portage && chown " + get_gentoomuch_uid() +  ":" + get_gentoomuch_uid() + ' ' + squashed_path + "'")
