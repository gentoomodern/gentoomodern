#!/usr/bin/env python3

import re
from .get_dockerized_profile_name import get_dockerized_profile_name

# Stuff all scripts here should use
debug = True
# First one first.
output_path                        = './gentoomuch-data/'
stages_path                        = output_path + 'stages/'
desired_stage_config_path	   = output_path + 'desired_stage'
desired_profile_config_path	   = output_path + 'desired_profile'
desired_packages_config_path       = output_path + 'desired_packages'
desired_hooks_config_path          = output_path + 'desired_hooks'
gpg_path                         = output_path + 'gpg/'
# Portage-related
portage_output_path                = output_path + 'portage/'
sets_output_path                   = portage_output_path + 'sets/'
patches_output_path                = portage_output_path + 'patches/'
# Include-related (for the program.) 
includes_path                      = './include/'
global_config_path                 = includes_path + 'portage.global/'
dockerfiles_path                   = includes_path + 'dockerfiles/'
# Config defines
config_path                        = './config/'
stage_defines_path                 = config_path + 'stage.defines/'
cpu_path                           = config_path + 'cpu.defines/'
pkgset_path                        = config_path + 'package.sets/'
patches_path                       = config_path + 'user.patches/'
local_config_basepath              = config_path + 'portage.locals/'
hooks_path                         = config_path + 'build.hooks/'
kernel_path                        = config_path + 'kernel.defines/'
arch_config_path                   = config_path + 'arch'
uid_config_path                    = config_path + 'uid'
gid_config_path                    = config_path + 'gid' # Need not exist, only for custom deployments

digests_ext = '.DIGESTS'
asc_ext =  digests_ext + '.asc'

# The beginning of the Docker image command.
image_tag_base                     = 'localhost:5000/gentoomuch-'
active_image_tag                   = image_tag_base + 'current:latest'
# The key to sign upstream releases
gentoo_signing_key                 = "0xBB572E0E2D182910"
# The url to obtain upstream releases
gentoo_upstream_url                = "https://ftp-osl.osuosl.org/pub/gentoo/releases/"
# Supported profiles (more platforms coming soon!)
profiles_amd64 = ( 'default', 'hardened+nomultilib', 'hardened-selinux+nomultilib', 'hardened-selinux', 'hardened', 'musl-hardened', 'musl-vanilla', 'nomultilib', 'systemd', 'uclibc-hardened', 'uclibc-vanilla', 'x32' )
# Names we can use when comparing strings to their Dockerized equivalents (no + or / symbols...)
profiles_amd64_dockerized          = { get_dockerized_profile_name(p) for p in profiles_amd64 }
