#!/usr/bin/env python3

import os

def sync_portage():
    os.system("docker-compose down && docker-compose up --no-start && docker-compose run gentoomuch-updater bash -c 'emerge --sync && emerge squashfs-tools && mksquashfs /var/db/repos/gentoo /mnt/squashed-portage/portage.squash'")
