#!/usr/bin/env python3

import os, sys, docker, re
from .gentoomodern_common import desired_packages_path, stages_path, output_path
from .read_file_lines import read_file_lines
from .write_file_lines import write_file_lines
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_docker_tag import get_docker_tag
from .swap_stage import swap_stage
from .get_local_tarball_name import get_local_tarball_name
from .containerize import containerize


def save_tarball(arch, profile, stage_define, upstream: bool):
    # Important to swap our active stage first!
    swap_stage(arch, profile, stage_define, bool(upstream))
    archive_name = get_local_tarball_name(arch, profile, stage_define)
    print("CREATING TARBALL: " + archive_name + " Using upstream image: " + str(upstream))
    if os.path.isfile(os.path.join(stages_path, archive_name)):
        os.remove(os.path.join(stages_path, archive_name))
    packages = []
    if os.path.isfile(desired_packages_path):
        packages = read_file_lines(desired_packages_path)
    packages_str = ''
    for l in packages:
        packages_str += l.strip()
        packages_str += ' '
    print('PACKAGES TO INSTALL : ' + packages_str)
      # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges. Then, it exits the chroot, unmounts all tempories, and packs a tarball as "stage3-<arch>-<base>-<user-stage-define>.tar.xz"
      # TODO: Parcel this out into smaller sections for manageability. The only real blocker here is the time it takes to test the command itself :P
    cmd_str = "cd " + output_path + " && "
    cmd_str += "docker-compose run gentoomodern-builder-privileged /bin/bash -c \""
    cmd_str += "emerge pigz && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "tar xpf /stage3-* --xattrs-include='*.*' --numeric-owner && "
    cmd_str += "rm -rf /mnt/gentoo/etc/portage/* && "
    cmd_str += "rsync -aXH /etc/portage/* /mnt/gentoo/etc/portage && "
    cmd_str += "mount -t proc none /mnt/gentoo/proc && "
    cmd_str += "mount -t tmpfs none /mnt/gentoo/tmp && "
    cmd_str += "mount --rbind /sys /mnt/gentoo/sys && "
    cmd_str += "mount --make-rslave /mnt/gentoo/sys && "
    cmd_str += "mount --rbind /dev /mnt/gentoo/dev && "
    cmd_str += "mount --make-rslave /mnt/gentoo/dev && "
    cmd_str += "mount -t tmpfs none /mnt/gentoo/var/tmp && "
    cmd_str += "mkdir -p /mnt/gentoo/var/tmp/portage && "
    cmd_str += "mount --bind /var/tmp/portage /mnt/gentoo/var/tmp/portage && "
    cmd_str += "mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && "
    cmd_str += "mkdir /mnt/gentoo/var/db/repos/gentoo && "
    cmd_str += "mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && "
    cmd_str += "echo 'UTC' > ./etc/timezone && "
    cmd_str += "echo 'nameserver 8.8.8.8' > ./etc/resolv.conf && "
    cmd_str += "chroot . /bin/bash -c '" # Enter chroot
    cmd_str += "env-update && "
    cmd_str += ". /etc/profile && "
    cmd_str += "emerge " + ("--emptytree " if upstream else "-uD --newuse --changed-use ") + packages_str + " @world && "
    cmd_str += "chown 1000:1000 -R /var/tmp/portage"
    cmd_str += "' && " # Exit chroot
    cmd_str += "chown 1000:1000 -R /var/tmp/portage && "
    # cmd_str += "umount -fl /mnt/gentoo/var/tmp/portage && "
    # cmd_str += "chown 1000:1000 -R /var/tmp/portage/* && "
    cmd_str += "umount -fl /mnt/gentoo/tmp && "
    cmd_str += "umount -fl /mnt/gentoo/proc && "
    cmd_str += "umount -fl /mnt/gentoo/sys && "
    cmd_str += "umount -fl /mnt/gentoo/dev && "
    cmd_str += "umount -fl /mnt/gentoo/var/db/repos/gentoo && "
    cmd_str += "umount -fl /mnt/gentoo/var/cache/binpkgs && "
    cmd_str += "umount -fl /mnt/gentoo/var/tmp/portage && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "tar -cvf /mnt/stages/" + archive_name + " . --use-compress-program=pigz --xattrs --selinux --numeric-owner --acls && "
    cmd_str += "chown 1000:1000 /mnt/stages/" + archive_name
    cmd_str +=  "\""
    code = os.system(cmd_str)
    if not code == 0:
        exit("FAILED TO CREATE TARBALL: " + archive_name)
    print('CREATING CONTAINER FROM: ' + archive_name)
    # The following call to containerize() had me a little tripped until thought of it. Here is why:
    #    It would be a mistake to passthrough the arguments' "upstream" variable in this particular context.
    #       By definition, a stage that's being saved from a Docker container has already been ingested and turned into something local.
    #    This property holds even when the binaries inside that dockerized stage come from upstream.
    results = containerize(archive_name, arch, profile, stage_define, bool(False))
    # Thus ends the deceptively simple-looking method call....
    if results and upstream:
        print("******************************************************************************************************************")
        print("***        CONGRATULATIONS! YOU HAVE JUST BOOTSTRAPPED A PROPER, OPTIMIZED, DOCKERIZED GENTOO STAGE3!          ***")
        print("******************************************************************************************************************")
        print("***                                                LIKE A BOSS!                                                ***")
        print("******************************************************************************************************************")
    return results
