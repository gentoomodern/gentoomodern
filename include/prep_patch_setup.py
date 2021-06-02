#!/usr/bin/env python3

import os
from .gentoomuch_common import saved_patches_path, working_patches_path


# Here, we will do the tooling required for you to start patching.
# This method creates the proper directory under ./config/user.patches
# Then it unpacks your ebuild into it, and initializes the git repository for patching
def setup_patch(patch_name, affected_package):
    # We first create the working directory
    p = os.path.join(working_patches_path, affected_package)
    os.makedirs(p, exist_ok = True)
    # Now we can spin up a docker and unpack that patch into the workdir
    ###
    ###

    ### ebuild $(portageq get_repo_path / gentoo)/sys-fs/lvm2/lvm2-2.02.145-r2.ebuild clean unpack
    ebuild_str = ''gt1
    ebuild_cmd_str = 'ebuild $(portageq ger_repo_path / gentoo)/' + 
    ### cd /var/tmp/portage/sys-fs/lvm2-2.02.145-r2/work/LVM2.2.02.145/
    ### git init
    ### git add .
    ### git commit
    ##### User does changes :P
    ### git diff | tee /tmp/foobar.patch
    ### git diff | grep -v '^diff\|^index' | tee /tmp/foobar.patch
    ##########
