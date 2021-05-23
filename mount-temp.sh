#!/bin/sh
#umount ./work/portage &
mount -t tmpfs none ./work/portage &&
mount -t tmpfs none ./work/stages &&
mount -t tmpfs none ./work/bootstrap &&
chown -R 1000:1000 ./work/portage &&
chown -R 1000:1000 ./work/bootstrap
