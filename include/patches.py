#!/usr/bin/env python3

import os, re, shutil, git
from .gentoomuch_common import output_path, portage_output_path, saved_patches_path, patches_workdir, patches_mountpoint, patches_in_progress_dir
from .get_gentoomuch_uid import get_gentoomuch_uid
from .get_arch import get_arch
from .swap_stage import swap_stage

#patches_in_progress_dir = os.path.relpath(patches_in_progress_dir, output_path)

def get_first_commit(repo_path):
    return "git -C " + repo_path + " log | grep commit | tail -2 | head -1 | sed -e 's/commit //g' "


def validate_package_format(package):
    if len(package.split('/')) < 2:
        print("setup_patch(): package name needs to be fully qualified. Got: " + package)
        return False
    return True


def get_patches_in_progress():
    if not os.path.isdir(patches_in_progress_dir):
        os.makedirs(patches_in_progress_dir, exist_ok = True)
    for root, dirs,files in os.walk(patches_in_progress_dir):
        for f in files:
            print(f)


def package_from_patch(patch_name : str) -> bool:
    candidate = os.path.join(patches_in_progress_dir, patch_name)
    print(candidate)
    if os.path.isfile(candidate):
        return (True, open(candidate, 'r').read().strip())
    return (False, '')


def send_diff(path_from: str, path_to : str, patch_name : str) -> bool:
    valid, versioned_package = package_from_patch(patch_name)
    if not valid == True:
        return False
    #print(versioned_package)
    p = os.path.join(path_from, patch_name, versioned_package)
    repo = git.Repo(p)
    # Get first commit.
    first_commit = list(repo.iter_commits('master'))[-1]
    num_backtracks = len(versioned_package.split('/'))
    # print("Backtracking: " + str(num_backtracks))
    backtrack_str = ''
    while num_backtracks > 0:
        backtrack_str += '../'
        num_backtracks -= 1
    final_output_dir = os.path.join(path_to, versioned_package)
    os.system("cd " + p + " && git diff " + first_commit.hexsha + " | grep -v '^diff\|^index' | tee ." + patch_name + ".patch")
    os.makedirs(final_output_dir, exist_ok = True)
    shutil.move(os.path.join(p, '.' + patch_name + '.patch'), os.path.join(final_output_dir, patch_name + '.patch'))
    return True

# Here, we will do the tooling required for you to start patching a given package+version
# Then it unpacks your ebuild into it, and initializes the git repository for patching
# The container uses local user privileges as defined on your system for the uid you set this tool to use.
# Note: The repo name is NOT (yet) saved as part of the process.
def prep_patch(patch_name: str, package: str, version: str, force: bool, repo_name: str = '') -> bool:
    if not validate_package_format(package):
        print("Could not validate package name: " + package)
        return False
    repo_name = 'gentoo' if repo_name == '' else repo_name
    versioned_package           = package + '-' + version
    versioned_package_notag     = re.sub('-r[0-9]+$', '', versioned_package)
    patch_export_hostdir        = os.path.join(patches_workdir, patch_name)
    if os.path.isdir(patch_export_hostdir) and len(os.listdir(patch_export_hostdir)) != 0:
        print("A patch-in-progress workdir already is present at " + patch_export_hostdir + " and is not empty!")
        return False
    else:
        os.makedirs(patch_export_hostdir, exist_ok = True)
    # For reference: ebuild $(portageq get_repo_path / gentoo)/ package-category/package-name/package-name-2.3-r7.ebuild clean unpack.
    cmd_str = 'PORTAGE_TMPDIR="' + patches_mountpoint + '" ebuild $(portageq get_repo_path / ' + repo_name + ')/' + package + '/' + versioned_package.split('/')[-1] + '.ebuild clean unpack && cd ' + patches_mountpoint + ' && '
    #################################################################################################################################
    # BASIC IDEA:
    # Here, we will clean up the directory by removing all non source-code items.
    # However, we also preserve most of the directory structure so as to slip the whole thing into a portage directory when needed.
    # First, we make certain we have the source code dir to the base.
    # Then, we clean out the one other directory.
    # Finally, we move all the source code itself down to the base and delete the old source code directory. Done. :P
    #################################################################################################################################
    temp_sourcedir                  = os.path.join(patches_mountpoint, 'TEMP')
    final_destination               = os.path.join(patches_mountpoint, versioned_package)
    where_all_the_actual_code_is    = os.path.join(patches_mountpoint, 'portage', versioned_package, 'work', '*')  #re.sub('-', '.', versioned_package_notag.split('/')[-1].upper()))
    # Now we assemble the actual command string.
    cmd_str += 'mkdir ' + temp_sourcedir + ' && mv ' + where_all_the_actual_code_is + '/* ' + temp_sourcedir + ' && rm -rf ' + os.path.join(patches_mountpoint, 'portage') + ' && mkdir -p ' + versioned_package  + ' && mv ' + temp_sourcedir + '/* ' + final_destination + ' && rmdir ' + temp_sourcedir
    # Now we can spin up a docker and unpack that patch into the workdir.
    swap_stage(get_arch(), 'default' , 'gentoomuch/builder', False, patch_name)
    code = os.system('cd ' + output_path  + ' &&  docker-compose run -u ' + get_gentoomuch_uid() + " gentoomuch-patcher /bin/bash -c '" + cmd_str + "'")
    # This appends the git commands we use to initiate the users' patch-making process.
    os.system('cd ' + os.path.join(patch_export_hostdir, versioned_package) + ' && git init && git add . && git commit -m "As-is from upstream (virgin.)"')
    # Debug messages.
    # print('Repo name:' + repo_name)
    # print("Unpacked sourcecode basedir: " + patches_mountpoint)
    # print('Pkg name (no tag): ' + versioned_package_notag)
    # print('Pkg name (with release tag): ' + versioned_package)
    # print('DEBUG: prep_patch(patch_name=' + patch_name + ', package=' + package + ', version=' + version + ', force=' + str(force) + ', repo_name=' + repo_name)
    # print("Patches mountpoint: " + patches_mountpoint)
    if code != 0:
        return False
    if not os.path.isdir(patches_in_progress_dir):
        os.makedirs(patches_in_progress_dir, exist_ok = True)
    open(os.path.join(patches_in_progress_dir, patch_name), 'w').write(versioned_package)
    return True


def list_available_package_versions(package: str, repo_name = ''):
    if not validate_package_format(package):
        exit("Could not read package version")
    repo_name = 'gentoo' if repo_name == '' else repo_name
    cmd_str = 'ls -alh$(portageq get_repo_path / ' + repo_name + ')/' + package
    code = os.system('cd ' + output_path + ' && docker-compose run -u ' + get_gentoomuch_uid() + " gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
    

# This method creates the proper directory under ./config/user.patches
def save_patch(patch_name : str, custom_output_path : str = '') -> bool:
    p = saved_patches_path if custom_output_path == '' else custom_output_path
    if os.path.isdir(p) and len(os.listdir(p)) == 0:
        print("While saving patch " + patch_name + ", we encountered a problem: Directory " + p + " exists and is not empty!")
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok = True)
    send_diff(patches_workdir, p, patch_name)
    return True


def try_patch(patch_name : str):
    valid, package_name = package_from_patch(patch_name)
    if not valid:
        print("Invalid patch name entered. Stopping.")
        return False
    patch_outdir = os.path.join(portage_output_path, 'patches')
    send_diff(patches_workdir, patch_outdir, patch_name)
    return True
