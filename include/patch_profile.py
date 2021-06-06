#!/usr/bin/env python3

import os, shutil
from .gentoomuch_common import output_path, portage_output_path, image_tag_base, active_image_tag, desired_packages_path, desired_hooks_path, output_path, topatch_config_path, saved_patches_path, patches_output_path
from .read_file_lines import read_file_lines


def patch_profile(arch, profile):
    p = os.path.join(topatch_config_path, arch, profile)
    if os.path.isfile(p):
        for candidate in read_file_lines(p):
            candidate_dir = os.path.join(saved_patches_path, candidate)
            if os.path.isdir(candidate_dir) and len(os.listdir(candidate_dir)) > 0:
                final_patches_output = os.path.join(patches_output_path, candidate)
                if os.path.isdir(final_patches_output):
                    os.system('rm -rf ' + final_patches_output)
                print("Applying patch: " + candidate)
                shutil.copy(candidate_dir, final_patches_output)
            else:
                exit("Cannot apply nonexistent patch: " + candidate)
