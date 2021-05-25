#!/usr/bin/env python3
import os, sys

class stage_serializer:
    def __init__(self, arch, profile, stage_define):
        self.dckr               = docker.from_env()
        self.arch               = arch
        self.profile            = profile
        self.stage_define       = stage_define
        self.archive_name       = 'stage3-' + self.arch + '-' + self.profile + '-' + self.stage_define
        self.extension          = '.tar'

    def save(self):
            needs_to_install_more_stuff = False
            packages = []
            archive_name = self.archive_name + self.extension 
            if os.path.isfile(os.path.join('./work/stages', archive_name)):
                os.remove(os.path.join('./work/stages', archive_name))
            packages_str = ''
            for l in packages:
                packages_str += l.strip()
                packages_str += ' '
            # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges everything with -K (binpkg-only). Then, it exists the chroot, unmounts all the chroot's temporary mounts, and creates from it a stage3 tarball under /mnt/stages/stage3-<arch>-<base>-xxxxx.tar.xz
            cmd_str = "cd work && docker-compose run gentoomuch-packer /bin/bash -c 'cd /mnt/gentoo && tar xpfv ../../stage3-*.tar.xz --xattrs-include=\'*.*\' --numeric-owner && mount -t proc none /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount -t tmpfs none /mnt/gentoo/tmp && mount -t tmpfs none /mnt/gentoo/var/tmp && rm -rf /mnt/gentoo/etc/stage_define/* && cp -R /etc/stage_define/* /mnt/gentoo/etc/stage_define && mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && mkdir /mnt/gentoo/var/db/repos/gentoo && mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && chroot . /bin/bash -c \"emerge -K --emptytree @world " + (packages_str if needs_to_install_more_stuff else "") + " &&  exit\" && umount -fl /mnt/gentoo/proc && umount -fl /mnt/gentoo/sys && umount -fl /mnt/gentoo/dev && umount -fl /mnt/gentoo/var/db/repos/gentoo && umount -fl /mnt/gentoo/var/cache/binpkgs && cd /mnt/gentoo && tar -cvf /mnt/stages/" + self.archive_name + self.extension + " . --xattrs --selinux --numeric-owner --acls && chown 1000:1000 /mnt/stages/" + self.archive_name + self.extension + "'"
            code = os.system(cmd_str)
            if code == 0:
                return True
            else:
                return False
        else:
            print('Could not open required config files.')
        return self.tarballed
    
    def containerize(self):
        os.system('cd ' + stages_path  + ' && docker import ' + self.archive_name + self.archive_ext + ' ' + image_tag_base + self.arch + '-' + self.basestage + '-' + self.stage_define + ':local ' )
