#!/bin/bash

umount -fl ./gentoomuch-data/ &
rm -rf ./gentoomuch-data/* &&
mount -t tmpfs none ./gentoomuch-data &&
mkdir ./gentoomuch-data/{portage,stages,bootstrap,gpg} &&
mount -t tmpfs none ./gentoomuch-data/{portage,stages,bootstrap,gpg} &&
chown -R 1000:1000 ./gentoomuch-data
