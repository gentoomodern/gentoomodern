#!/bin/sh
umount gentoomuch-data/squashed/mountpoint &
mount gentoomuch-data/squashed/blob/portage.squash gentoomuch-data/squashed/mountpoint -t squashfs -o loop
