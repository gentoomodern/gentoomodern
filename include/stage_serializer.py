#!/usr/bin/env python3

import os, sys, docker
from .gentoomuch_common import desired_packages_path, stages_path, read_file_lines, output_path, get_cleaned_profile, get_cleaned_stagedef
from .get_docker_tag import get_docker_tag

class stage_serializer:
  def __init__(self, arch, profile, stage_define):
    self.dckr               = docker.from_env()
    self.arch               = arch
    self.profile            = get_cleaned_profile(profile)
    self.stage_define       = get_cleaned_stagedef(stage_define)
    self.archive_name       = 'stage3-' + self.arch + '-' + self.profile + '-' + self.stage_define + '.tar'
    print('DEBUG: ' + self.archive_name)

  def save_tarball(self):
    needs_to_install_more_stuff = False
    packages = []
    if os.path.isfile(desired_packages_path):
        packages = read_file_lines(desired_packages_path)
    if os.path.isfile(os.path.join(stages_path, archive_name)):
        os.remove(os.path.join(stages_path, archive_name))
    packages_str = ''
    for l in packages:
        packages_str += l.strip()
        packages_str += ' '
    if len(packages) > 0:
        needs_to_install_more_stuff = True
      # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges everything with -K (binpkg-only). Then, it exists the chroot, unmounts all the chroot's temporary mounts, and creates from it a stage3 tarball under /mnt/stages/stage3-<arch>-<base>-xxxxx.tar.xz
    cmd_str = "cd " + output_path + " && docker-compose run gentoomuch-packer /bin/bash -c 'mount -t tmpfs none /mnt/gentoo && cd /mnt/gentoo && tar xpfv ../../stage3-*.tar.xz --xattrs-include=\'*.*\' --numeric-owner && mount -t proc none /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount -t tmpfs none /mnt/gentoo/tmp && mount -t tmpfs none /mnt/gentoo/var/tmp && mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && mkdir /mnt/gentoo/var/db/repos/gentoo && mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && chroot . /bin/bash -c \"echo 'UTC' > /etc/timezone && emerge -K --emptytree @world " + (packages_str if needs_to_install_more_stuff else "") + " &&  exit\" && umount -fl /mnt/gentoo/proc && umount -fl /mnt/gentoo/sys && umount -fl /mnt/gentoo/dev && umount -fl /mnt/gentoo/var/db/repos/gentoo && umount -fl /mnt/gentoo/var/cache/binpkgs && cd /mnt/gentoo && tar -cvf /mnt/stages/" + self.archive_name + " . --xattrs --selinux --numeric-owner --acls && cd / && umount -fl /mnt/gentoo && chown 1000:1000 /mnt/stages/" + self.archive_name + "'"
    code = os.system(cmd_str)
    
  def containerize(self):
    os.system('cd ' + stages_path  + ' && docker import ' + self.archive_name + ' ' + get_docker_tag(self.arch, self.profile, self.stage_define))

  #def delete_tarball(self):
  #  os.system('cd ' + stages_path  + ' && rm ' + self.archive_name)
