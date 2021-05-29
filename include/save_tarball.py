#!/usr/bin/env python3

import os, sys, docker, re
from .gentoomuch_common import desired_packages_path, stages_path, output_path
from .read_file_lines import read_file_lines
from .write_file_lines import write_file_lines
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_docker_tag import get_docker_tag
from .swap_stage import swap_stage
from .get_tarball_name import get_tarball_name


def save_tarball(arch, profile, stage_define, upstream = False):
    swap_stage(arch, profile, stage_define, upstream)
    archive_name = get_tarball_name(arch, profile, stage_define, upstream)
    print("CREATING TARBALL: " + archive_name)
    packages = []
    if os.path.isfile(desired_packages_path):
        packages = read_file_lines(desired_packages_path)
    if os.path.isfile(os.path.join(stages_path, archive_name)):
        os.remove(os.path.join(stages_path, archive_name))
    packages_str = ''
    for l in packages:
        packages_str += l.strip()
        packages_str += ' '
      # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges everything with -K (binpkg-only). Then, it exists the chroot, unmounts all the chroot's temporary mounts, and creates from it a stage3 tarball under /mnt/stages/stage3-<arch>-<base>-xxxxx.tar.xz
      # TODO: Parcel this out into smaller sections for manageability.
    cmd_str = "cd " + output_path + " && docker-compose run gentoomuch-builder /bin/bash -c \"mount -t tmpfs gentoomuch_serializer_temp_root /mnt/gentoo && cd /mnt/gentoo && tar xpfv /stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner && mount -t proc gentoomuch_serializer_temp_proc /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount -t tmpfs gentoomuch_serializer_tmp /mnt/gentoo/tmp && mount -t tmpfs gentoomuch_serializer_var_tmp /mnt/gentoo/var/tmp && mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && mkdir /mnt/gentoo/var/db/repos/gentoo && mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && echo 'UTC' > ./etc/timezone && echo 'nameserver 8.8.8.8' > ./etc/resolv.conf && mount --rbind /etc/portage ./etc/portage && chroot . /bin/bash -c 'env-update && . /etc/profile && emerge --emptytree @world && " + (" emerge -uD --changed-use " + packages_str + " && " if len(packages_str) > 0 else "") + " exit' && umount -fl /mnt/gentoo/proc && umount -fl /mnt/gentoo/sys && umount -fl /mnt/gentoo/dev && umount -fl /mnt/gentoo/var/db/repos/gentoo && umount -fl /mnt/gentoo/var/cache/binpkgs && umount -fl /mnt/gentoo/etc/portage && cd /mnt/gentoo && tar -cvJf /mnt/stages/" + archive_name + " . --xattrs " + (" --selinux " if re.match("selinux", profile) else "") + " --numeric-owner --acls && cd / && chown 1000:1000 /mnt/stages/" + archive_name + "\""
    code = os.system(cmd_str)
    if not code == 0:
        exit("FAILED TO CREATE TARBALL: " + archive_name)
    print('SAVING TARBALL: ' + archive_name)
    code = os.system('cd ' + stages_path  + ' && docker import ' + archive_name + ' ' + get_docker_tag(arch, profile, stage_define))
    if not code == 0:
        return False
