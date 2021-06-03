#!/usr/bin/env python3

import os, re
from .gentoomuch_common import output_path, saved_patches_path, patches_workdir, patches_mountpoint
from .get_gentoomuch_uid import get_gentoomuch_uid
from .get_arch import get_arch

def get_first_commit():
    return "git log | grep commit | tail -2 | head -1 | sed -e 's/commit //g'"

def validate_pkgname(package):
    if len(package.split('/')) < 2:
        print("setup_patch(): package name needs to be fully qualified.")
        print(package.split('/'))
        return False
    return True

def setup_git_user():
    return ' git config --global user.email "gentoomuch-user@temporary.localhost" && git config --global user.name "Gentoomuch User" '

# Here, we will do the tooling required for you to start patching a given package+version
# Then it unpacks your ebuild into it, and initializes the git repository for patching
def prep_patch(patch_name: str, package_arg: str, version: str, force: bool, repo_name: str = '') -> bool:
    # swap_stage(get_arch(), 'default' , 'gentoomuch/builder', false) # 
    if not validate_pkgname(package_arg):
        print("Could not validate package name: " + package_arg)
        return False
    print('DEBUG: prep_patch(patch_name=' + patch_name + ', package=' + package_arg + ', version=' + version + ', force=' + str(force) + ', repo_name=' + repo_name)
    repo_name = 'gentoo' if repo_name == '' else repo_name
    print('Repo name:' + repo_name)
    pkgname = package_arg + '-' + version
    print('Pkg name (with release tag): ' + pkgname)
    pkgname_notag = re.sub('-r[0-9]+$', '', pkgname)
    print('Pkg name (no tag): ' + pkgname_notag)
    # We first create the working directory
    patches_basepath = os.path.join(patches_workdir, patch_name)
    ebuilds = os.path.join(patches_basepath, repo_name)
    os.makedirs(ebuilds, exist_ok = True)
    # Now we can spin up a docker and unpack that patch into the workdir
    ### ebuild $(portageq get_repo_path / gentoo)/ sys-fs/lvm2/lvm2-2.02.145-r2.ebuild clean unpack
    unpacked_sourcecode_basedir = os.path.join(patches_mountpoint, patch_name, 'gentoo' if repo_name == '' else repo_name)#, pkgname, 'work', pkgname_notag.upper().split('/')[-1])
    
    print("Unpacked sourcecode basedir: " + unpacked_sourcecode_basedir)
    # new_source_location = os.path.join(patches_mountpoint, patch_name) if repo_name == '' else os.path.join(patches_mountpoint, repo_name, patch_name) 
    # print("New sourcecode location: " + new_source_location)
    print("Patches mountpoint: " + patches_mountpoint)
    #if os.path.isdir(new_source_location) and len(os.listdir(new_source_location)) > 0:
    #    print("Working directory for patch " + new_source_location + " already exists and is not empty!")
    #    return False


    # This thing exports (non-privileged users' directory bind-mounted to our workdir) the source code repo. It also initializes a git repo.
    cmd_str = 'PORTAGE_TMPDIR="' + unpacked_sourcecode_basedir + '" ebuild $(portageq get_repo_path / ' + repo_name + ')/' + package_arg + '/' + pkgname.split('/')[-1] + '.ebuild clean unpack && cd ' + unpacked_sourcecode_dir + ' && ' + setup_git_user() + ' && git init && git add . && git commit -m "As-is from upstream (virgin.)"'  #&& mkdir -p ' + new_source_location + ' && mv ./* ' + new_source_location + ' && cd ' + patches_mountpoint + ' && rm -rf ' + package_arg.split('/')[0] + '\n'
    code = os.system('cd ' + output_path  + ' &&  docker-compose run -u ' + get_gentoomuch_uid() + ' gentoomuch-patcher /bin/bash -c \'' + cmd_str + '\'')
    if code != 0:
        return False
    return True


def list_available_package_versions(package: str, repo_name = '') -> bool:
    cmd_str = 'ls $(portageq get_repo_path / ' + repo_name + ')/' + package
    code = os.system('cd ' + output_path + ' && docker-compose run -u ' + get_gentoomuch_uid() + ' gentoomuch-builder /bin/bash -c \'' + cmd_str + '\'')

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
    return False
