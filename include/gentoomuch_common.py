#!/usr/bin/env python3

import re
from .get_cleaned_profile import get_cleaned_profile

# Stuff all scripts here should use
debug = True
output_path                 = './gentoomuch-data/'
stages_path                 = output_path + 'stages/'
portage_output_path         = output_path + 'portage/'
desired_stage_path	    = output_path + 'desired_stage'
desired_profile_path	    = output_path + 'desired_profile'
desired_packages_path       = output_path + 'desired_packages'
desired_hooks_path          = output_path + 'desired_hooks'
sets_output_path            = portage_output_path + 'sets/'
patches_output_path         = portage_output_path + 'patches/'
includes_path               = './include/'
global_config_path          = includes_path + 'portage.global/'
dockerfiles_path            = includes_path + 'dockerfiles/'
config_path                 = './config/'
stage_defines_path          = config_path + 'stage.defines/'
cpu_path                    = config_path + 'cpu.defines/'
pkgset_path                 = config_path + 'package.sets/'
patches_path                = config_path + 'user.patches/'
local_config_basepath       = config_path + 'portage.locals/'
hooks_path                  = config_path + 'build.hooks/'
kernel_path                 = config_path + 'kernel.defines/'
arch_config_path            = config_path + 'arch'
uid_config_path             = config_path + 'uid'
gid_config_path             = config_path + 'gid' # Need not exist, only for custom deployments
image_tag_base              = 'localhost:5000/gentoomuch-'
active_image_tag            = image_tag_base + 'current:latest'

gentoo_signing_key          = "0xBB572E0E2D182910"


profiles_amd64 = ( 'default', 'hardened+nomultilib', 'hardened-selinux+nomultilib', 'hardened-selinux', 'hardened', 'musl-hardened', 'musl-vanilla', 'nomultilib', 'systemd', 'uclibc-hardened', 'uclibc-vanilla', 'x32' )

profiles_amd64_cleaned = { get_cleaned_profile(p) for p in profiles_amd64 }
