#!/usr/bin/env python3

# This saves out a named tarball of a given stage define.
import os, sys, re, docker
from include.gentoomuch_common import read_file_lines, write_file_lines, arch_config_path, current_basestage_path, current_portage_path
from include.portage_directory_combiner import portage_directory_combiner

class stage_serializer:

    def __init__(self, is_upstream):
        self.upstream   = is_upstream
        self.dckr       = docker.from_env()
        self.dckr_imgs  = self.dckr.images.list()
    
    def containerize(self):
        if os.path.isfile(arch_config_path) and os.path.isfile(current_basestage_path) and os.path.isfile(current_portage_path):
            arch = open(arch_config_path).read().strip()
            current_basestage = open(current_basestage_path).read().strip()
            current_portage = open(current_portage_path).read().strip()
            archive_name = 'stage3-' + arch + '-' + current_basestage + '-' + re.sub('/', '-', current_portage) + '.tar.xz'
            if os.path.isfile(os.path.join('./work/stages', archive_name)):
                os.remove(os.path.join('./work/stages', archive_name))
            # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges everything with -K. Then, it exists the chroot, unmounts all the chroot's temporary mounts, and creates from it a stage3 tarball under /mnt/stages/stage3-<arch>-<base>-xxxxx.tar.xz
            cmd_str = "docker-compose run gentoomuch-packer /bin/bash -c 'eselect profile list && cd /mnt/gentoo && tar xpfv ../../stage3-*.tar.xz --xattrs-include=\'*.*\' --numeric-owner && mount -t proc none /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount -t tmpfs none /mnt/gentoo/tmp && mount -t tmpfs none /mnt/gentoo/var/tmp && rm -rf /mnt/gentoo/etc/portage/* && cp -R /etc/portage/* /mnt/gentoo/etc/portage && mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && mkdir /mnt/gentoo/var/db/repos/gentoo && mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && chroot . /bin/bash -c \"emerge -K --emptytree @world && exit\" && umount -fl /mnt/gentoo/proc && umount -fl /mnt/gentoo/sys && umount -fl /mnt/gentoo/dev && umount -fl /mnt/gentoo/var/db/repos/gentoo && umount -fl /mnt/gentoo/var/cache/binpkgs && tar -cJvf /mnt/stages/" + archive_name + " /mnt/gentoo/* --xattrs --selinux --acls'"
            os.system(cmd_str)
        else:
            print('Could not open required config files.')




stage_serializer(True).containerize()
