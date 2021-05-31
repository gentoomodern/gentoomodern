#!/usr/bin/env python3

import os, sys, re
from .gentoomuch_common import output_path, config_path, active_image_tag, stages_path
from .write_file_lines import write_file_lines
from .get_active_stage import get_active_stage
from .tag_parser import tag_parser


builder_str = 'builder'
updater_str = 'updater'

# This uses the current state of the work/portage directory and automatically creates a composefile that'll properly include each file. This avoids much handcruft.
def create_composefile(output_path):
    lines = ['# Do not make changes to this file, as they will be overriden upon the next build.\n' , 'services:\n']
    lines.extend(__output_config(builder_str))
    lines.extend(__output_config(updater_str))
    include_prefix = 'include/docker-compose/docker-compose.'
    lines.append('networks:\n')
    lines.append('  backend:\n')
    lines.append('    driver: overlay\n')
    lines.append('volumes:\n')
    lines.append('  distfiles:\n')
    lines.append('    driver: local\n')
    lines.append('  ebuilds:\n')
    lines.append('    driver: local\n')
    lines.append('  binpkgs:\n')
    lines.append('    driver: local\n')
    lines.append('  kernels:\n')
    lines.append('    driver: local\n')
    write_file_lines(os.path.join(output_path, 'docker-compose.yml'), lines)

def __output_config(container_type_str):
    if not container_type_str == builder_str and not container_type_str == updater_str:
        sys.exit('Gentoomuch.create-composefile: Invalid container type argument \"' + container_type_str  +  '\"')
    is_builder  = bool(container_type_str == builder_str)
    is_updater  = bool(container_type_str == updater_str)
    # Our results will be a list of strings.
    results = [] 
    # First, we define whether this'll be a builder or a packer.
    results.append('  gentoomuch-' + container_type_str + ':\n')
    # We append the universal parts.
    results.append('    # The following line is a cool trick that fools the docker program into using a locally-tagged image as if it came from a proper repository.\n')
    results.append('    image: ' + active_image_tag + '\n')
    results.append('    command: /bin/bash\n')
    results.append('    networks:\n')
    results.append('    - backend\n')
    results.append('    volumes:\n')
    results.append('    - /dev:/dev\n')
    results.append('    - /proc:/proc\n')
    results.append('    - /sys:/sys:ro\n')
    # These are parts that have different permissions between the two types of containers.
    binpkg_str          = '    - binpkgs:/var/cache/binpkgs'
    distfiles_str       = '    - distfiles:/var/cache/distfiles'
    ebuilds_str         = '    - ebuilds:/var/db/repos/gentoo'
    kernels_str         = '    - kernels:/mnt/kernels'
    squashed_output_str = '    - ./squashed/blob:/mnt/squashed-portage'
    squashed_mount_str  = '    - ./squashed/mountpoint:/mnt/squashed-portage'
    stages_mount_str    = '    - ./stages:/mnt/stages'
    # Here we actually write these differential parts into our list.
    if is_builder:
        results.append(binpkg_str + '\n')
        results.append(distfiles_str +'\n')
        results.append(ebuilds_str + '\n')
        results.append(kernels_str + '\n')
        results.append(squashed_mount_str + '\n')
        results.append(stages_mount_str + '\n')
    if is_updater:
        results.append(binpkg_str + '\n')
        results.append(distfiles_str +'\n')
        results.append(ebuilds_str + '\n')
        results.append(kernels_str + '\n')
        results.append(squashed_output_str + '\n')
        results.append(stages_mount_str + ':ro\n')
    # This one is added at the end for consistency of end-users' reading. It does NOT require multiple types of permissions.
    results.append('    - ./emerge-logs:/var/log/portage\n')
    # Here we loop over the all the files in the config/portage directory and add them.
    portage_tgt = '/etc/portage/'
    for (dirpath, directories, files) in os.walk(output_path + 'portage'):
        for f in files:
            if not f[0] == '.' and not f == 'README.md':
                rel_path = os.path.relpath(dirpath, output_path)
                results.append('    - ./' + os.path.join(rel_path, f) + ':' + os.path.join('/etc/', rel_path, f) + ':ro\n')
    if is_builder:
        results.append('    cap_add:\n')
        results.append('    - CAP_SYS_ADMIN\n')
        results.append('    - CAP_NET_ADMIN\n')
    # Finally, we return the list of string.
    return results
