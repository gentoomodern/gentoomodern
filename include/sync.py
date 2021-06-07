#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path
from .get_gentoomuch_uid import get_gentoomuch_uid

def sync():
    squashed_path = '/mnt/squashed-portage/portage.squash'
    uid = get_gentoomuch_uid()
    os.system("cd " + output_path + " && docker-compose run gentoomuch-updater /bin/bash -c 'rm " + squashed_path + " & emerge -v --sync && emerge squashfs-tools && mksquashfs /var/db/repos/gentoo " + squashed_path + " -noappend -force-gid portage -force-uid portage && chown " + uid +  ":" + uid + ' ' + squashed_path + "'")
