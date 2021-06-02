#!/usr/bin/env python3

import os, re
from .gentoomuch_common import saved_patches_path, host_ebuild_export_path, patches_mountpoint
from .get_gentoomuch_uid import get_gentoomuch_uid


def get_first_commit():
    return "git log | grep commit | tail -2 | head -1 | sed -e 's/commit //g'"


# Here, we will do the tooling required for you to start patching a given package+version
# Then it unpacks your ebuild into it, and initializes the git repository for patching
def prep_patch(patch_name: str, package: str, version: str, force: bool, repo_name = '') -> bool:
    if os.path.dirname(package) == '':
        print("setup_patch(): package name needs to be fully qualified."
        return False
    repo_name = 'gentoo' if repo_name == '' else repo_name
    print('Repo name:' + repo_name)
    pkgname = package + '-' + version
    print('Pkg name (with release tag): ' + pkgname)
    print('Pkg name (no tag): ' + pkgname_notag)
    pkgname_notag = re.sub(pkgname, '', '-r\d+^')
    # We first create the working directory
    patches_basepath = os.path.join(working_patches_path, patch_name)
    ebuilds = os.path.join(patches_basepath, repo_name)
    os.makedirs(ebuilds, exist_ok = True)
    # Now we can spin up a docker and unpack that patch into the workdir
    ### ebuild $(portageq get_repo_path / gentoo)/ sys-fs/lvm2/lvm2-2.02.145-r2.ebuild clean unpack
    unpacked_sourcecode_dir = os.path.join(patches_mountpoint, pkgname, 'work', pkgname_notag.upper())
    new_source_location = os.path.join(patches_mountpoint, patch_name)
    if os.path.isdir(new_source_location) and len(os.listdir(new_source_location)) > 0:
        print("Working directory for patch " + new_source_code_location + " already exists and is not empty!"))
        return False
    # This thing exports (non-privileged users' directory bind-mounted to our workdir) the source code repo. It also initializes a git repo.
    cmd_str = 'PORTAGE_TMPDIR="' + patches_mountpoint + '" ebuild $(portageq get_repo_path / ' + repo_name + ')/' + pkgname + '.ebuild clean unpack && cd ' + patches_mountpoint + ' && cd ' + unpacked_sourcecode_dir + ' && git init && git add . && git commit -m "As-is from upstream (virgin.)" && mkdir ' + new_source_location + ' && mv ./* ' + new_source_location + ' && cd ' + patches_mountpoint + ' && rm -rf ' + package.split('/')[0] + '\n'
    code = os.system('cd ' + output_path  + ' &&  docker-compose run -u ' + get_gentoomuch_uid() + ' gentoomuch-builder /bin/bash -c \'' + cmd_str + '\'')
    if code != 0:
        return False
    return True

# This method creates the proper directory under ./config/user.patches
def save_patch(package: str, version: str, repo_name = '') -> bool:
    return False

def try_patch(package: str, version: str, repo_name = '') -> bool:
    ### cd /var/tmp/portage/sys-fs/lvm2-2.02.145-r2/work/LVM2.2.02.145/
    ##### User does changes. I can't do that for you. :P
    ########## Send the patch out.
    ### git diff | tee /tmp/foobar.patch
    ########## Cleanup
    ### git diff | grep -v '^diff\|^index' | tee /tmp/foobar.patch
    ##########
