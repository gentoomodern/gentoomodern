#!/bin/sh
#umount ./gentoomuch-data/portage &
mount -t tmpfs none ./gentoomuch-data/portage &&
mount -t tmpfs none ./gentoomuch-data/stages &&
mount -t tmpfs none ./gentoomuch-data/bootstrap &&
chown -R 1000:1000 ./gentoomuch-data/portage &&
chown -R 1000:1000 ./gentoomuch-data/stages &&
chown -R 1000:1000 ./gentoomuch-data/bootstrap
