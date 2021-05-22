#!/usr/bin/env python3

# This saves out a named tarball of a given stage define.
import os, sys, re, shutil, docker
from include.gentoomuch_common import read_file_lines, write_file_lines, arch_config_path, current_basestage_path, includes_path, current_portage_path, stages_path, dockerfiles_path
from include.portage_directory_combiner import portage_directory_combiner

class stage_serializer:

    def __init__(self):
        self.dckr               = docker.from_env()
        self.tarballed          = False
    
    def save_stage(self):
        if os.path.isfile(arch_config_path) and os.path.isfile(current_basestage_path) and os.path.isfile(current_portage_path):
            arch = open(arch_config_path).read().strip()
            current_basestage = open(current_basestage_path).read().strip()
            current_portage = open(current_portage_path).read().strip()
            archive_name = 'stage3-' + arch + '-' + current_basestage + '-' + re.sub('/', '-', current_portage) + '.tar.gz'
            needs_to_install_more_stuff = False
            packages = []
            if os.path.isfile('./config/packages'):
                needs_to_install_more_stuff = True
                packages = read_file_lines('./config/packages')
            if os.path.isfile(os.path.join('./work/stages', archive_name)):
                os.remove(os.path.join('./work/stages', archive_name))
            packages_str = '&& emerge -K '
            for l in packages:
                packages_str += l.strip()
                packages_str += ' '
            # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges everything with -K. Then, it exists the chroot, unmounts all the chroot's temporary mounts, and creates from it a stage3 tarball under /mnt/stages/stage3-<arch>-<base>-xxxxx.tar.xz
            cmd_str = "docker-compose run gentoomuch-packer /bin/bash -c 'eselect profile list && cd /mnt/gentoo && tar xpfv ../../stage3-*.tar.xz --xattrs-include=\'*.*\' --numeric-owner && mount -t proc none /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount -t tmpfs none /mnt/gentoo/tmp && mount -t tmpfs none /mnt/gentoo/var/tmp && rm -rf /mnt/gentoo/etc/portage/* && cp -R /etc/portage/* /mnt/gentoo/etc/portage && mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && mkdir /mnt/gentoo/var/db/repos/gentoo && mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && chroot . /bin/bash -c \"emerge -K --emptytree @world " + (packages_str if needs_to_install_more_stuff else "") + " &&  exit\" && umount -fl /mnt/gentoo/proc && umount -fl /mnt/gentoo/sys && umount -fl /mnt/gentoo/dev && umount -fl /mnt/gentoo/var/db/repos/gentoo && umount -fl /mnt/gentoo/var/cache/binpkgs && GZIP=-9 tar -czvf /mnt/stages/" + archive_name + " /mnt/gentoo/* --xattrs --selinux --acls && chown 1000:1000 /mnt/stages/" + archive_name + "'"
            code = os.system(cmd_str)
            if code == 0:
                self.tarballed = True
        else:
            print('Could not open required config files.')
        return self.tarballed

    def containerize(self, architecture, base_profile, user_stage):
        # TODO: Build from Dockerfile using self.dckr
        shutil.copyfile(os.path.join(dockerfiles_path, 'local', 'Dockerfile.part1'), os.path.join(stages_path, 'Dockerfile'))
        i =self.dckr.images.build(path = stages_path, buildargs = {'ARCH': open(arch_config_path).read().strip(), 'PROFILE': open(current_basestage_path).read().strip(), 'USER': re.sub('/', '-', open(current_portage_path).read().strip())}, tag =  'gentoomuch-bootstrap:latest')
        i[0].tag('gentoomuch-bootstrap', 'latest')
        img_name = 'stage3-' + architecture + '-' + base_profile + '-' + user_stage
        # Here we copy the unpacked things into a blank container, and we win the game!
        self.dckr.images.build(path = os.path.join(includes_path, 'dockerfiles/pull'), dockerfile = 'step4.Dockerfile', tag = img_name)

#stage_serializer(True).save_stage()
im_serial_guys = stage_serializer()
#im_serial_guys.save_stage()
im_serial_guys.containerize('amd64', 'default', 'gentoomuch-builder') 
