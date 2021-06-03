#!/usr/bin/env python3

import os, re
from .gentoomuch_common import output_path, saved_patches_path, patches_workdir, patches_mountpoint
from .get_gentoomuch_uid import get_gentoomuch_uid
from .get_arch import get_arch
from .swap_stage import swap_stage


def get_first_commit():
    return "git log | grep commit | tail -2 | head -1 | sed -e 's/commit //g'"


def validate_pkgname(package):
    if len(package.split('/')) < 2:
        print("setup_patch(): package name needs to be fully qualified.")
        print(package.split('/'))
        return False
    return True


#def get_desired_patch() -> str:
#    config = os.path.join(output_path, 'desired_patch')

# def set_desired_patch():
    # config = os.path.join(output_path, 'desired_patch')    

def setup_git_user() -> str:
    return ' git config --global user.email "gentoomuch-user@temporary.localhost" && git config --global user.name "Gentoomuch User" '


# def get_unpacked_ebuild_basepath(repo_name: str, package_arg: arg, version: str, unpacked_sourcecode_dir: str = '') -> str:


# def unpack_ebuild(repo_name: str, package_arg : str, version : str,  unpacked_sourcecode_dir : str = '') -> str:


# def get_ebuild_source_dir(repo_name : str, package_arg : str, version : str, unpacked_sourcecode_dir: str = '') -> str:






# Here, we will do the tooling required for you to start patching a given package+version
# Then it unpacks your ebuild into it, and initializes the git repository for patching
# The container uses local user privileges as defined on your system for the uid you set this tool to use.
def prep_patch(patch_name: str, package_arg: str, version: str, force: bool, repo_name: str = '') -> bool:
    if not validate_pkgname(package_arg):
        print("Could not validate package name: " + package_arg)
        return False
    repo_name = 'gentoo' if repo_name == '' else repo_name
    pkgname = package_arg + '-' + version
    pkgname_notag = re.sub('-r[0-9]+$', '', pkgname)
    patch_export_hostdir = os.path.join(patches_workdir, patch_name)
    if os.path.isdir(patch_export_hostdir):
        print("Patch-in-progress workdir already present at " + patch_export_hostdir)
        return False
    else:
        os.makedirs(patch_export_hostdir)
    # We first create the working directory
    unpacked_sourcecode_basedir = patches_mountpoint #os.path.join(patches_mountpoint, patch_name)
    # os.system('cd ' + patches_workdir + ' && rm -rf ./*')
    # For reference: ebuild $(portageq get_repo_path / gentoo)/ package-category/package-name/package-name-2.3-r7.ebuild clean unpack.
    cmd_str = 'PORTAGE_TMPDIR="' + unpacked_sourcecode_basedir + '" ebuild $(portageq get_repo_path / ' + repo_name + ')/' + package_arg + '/' + pkgname.split('/')[-1] + '.ebuild clean unpack && cd ' + unpacked_sourcecode_basedir + ' && ls -alh  && '
    #################################################################################################################################
    # BASIC IDEA:
    # Here, we will clean up the directory by removing all non source-code items.
    # However, we also preserve most of the directory structure so as to slip the whole thing into a portage directory when needed.
    # First, we make certain we have the source code dir to the base.
    # Then, we clean out the one other directory.
    # Finally, we move all the source code itself down to the base and delete the old source code directory. Done. :P
    #################################################################################################################################
    temp_sourcedir                  = os.path.join(unpacked_sourcecode_basedir, 'TEMP')
    final_destination               = os.path.join(unpacked_sourcecode_basedir, package_arg)
    where_all_the_actual_code_is    = os.path.join(unpacked_sourcecode_basedir, 'portage', pkgname, 'work', re.sub('-', '.', pkgname_notag.split('/')[-1].upper()))
    # Now we assemble the actual command string.
    cmd_str += 'mkdir ' + temp_sourcedir + ' && mv ' + where_all_the_actual_code_is + '/* ' + temp_sourcedir + ' && rm -rf ' + os.path.join(unpacked_sourcecode_basedir, 'portage') + ' && mkdir -p ' + package_arg  + ' && mv ' + temp_sourcedir + '/* ' + final_destination + ' && rmdir ' + temp_sourcedir + ' && cd ' + final_destination + ' && '
    # This appends the git commands we use to initiate the users' patch-making process.
    cmd_str += setup_git_user() + ' && git init && git add . && git commit -m "As-is from upstream (virgin.)"'
    # Now we can spin up a docker and unpack that patch into the workdir.
    swap_stage(get_arch(), 'default' , 'gentoomuch/builder', False, patch_name)
    code = os.system('cd ' + output_path  + ' &&  docker-compose run -u ' + get_gentoomuch_uid() + ' gentoomuch-patcher /bin/bash -c \'' + cmd_str + '\'')
    # Debug messages.
    print('Repo name:' + repo_name)
    print("Unpacked sourcecode basedir: " + unpacked_sourcecode_basedir)
    print('Pkg name (no tag): ' + pkgname_notag)
    print('Pkg name (with release tag): ' + pkgname)
    print('DEBUG: prep_patch(patch_name=' + patch_name + ', package=' + package_arg + ', version=' + version + ', force=' + str(force) + ', repo_name=' + repo_name)
    print("Patches mountpoint: " + patches_mountpoint)
    if code != 0:
        return False
    return True


def list_available_package_versions(package: str, repo_name = ''):
    cmd_str = 'ls $(portageq get_repo_path / ' + repo_name + ')/' + package
    code = os.system('cd ' + output_path + ' && docker-compose run -u ' + get_gentoomuch_uid() + " gentoomuch-builder /bin/bash -c '" + cmd_str + "'")


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
