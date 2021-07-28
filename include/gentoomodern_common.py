#!/usr/bin/env python3

import re, os
from .get_dockerized_profile_name import get_dockerized_profile_name


#Stuff all scripts here should use
debug				        = True
output_path				    = './gentoomodern-data'
stages_path		            = os.path.join(output_path, 'stages')
gpg_path				    = os.path.join(output_path, 'gpg')
squashed_path               = os.path.join(output_path, 'squashed')
emergelogs_path             = os.path.join(output_path, 'emerge.logs')
patches_workdir             = os.path.join(output_path, 'patches')
env_output_path             = os.path.join(output_path, 'env')
desired_stage_path		    = os.path.join(env_output_path, 'desired_stage')
desired_profile_path	    = os.path.join(env_output_path, 'desired_profile')
desired_packages_path    	= os.path.join(env_output_path, 'desired_packages')
desired_hooks_path			= os.path.join(env_output_path, 'desired_hooks')
patches_in_progress_dir     = os.path.join(env_output_path, 'patches')
# Portage-related
portage_output_path		    = os.path.join(output_path, 'portage')
sets_output_path	    	= os.path.join(portage_output_path, 'sets')
patches_output_path        	= os.path.join(portage_output_path, 'patches')
# Includes (immutable data)
includes_path				= './include'
global_portage_config_path  = os.path.join(includes_path, 'portage.global')
dockerfiles_path		    = os.path.join(includes_path, 'dockerfiles')
# Config defines, local
config_path			        = './config/local'
stage_defines_path	        = os.path.join(config_path, 'stage.defines')
kernel_defines_path         = os.path.join(config_path, 'kernel.defines')
system_defines_path         = os.path.join(config_path, 'system.defines')
buildhook_defines_path	    = os.path.join(config_path, 'buildhook.defines')
cpu_frags_path			    = os.path.join(config_path, 'cpu.frags')
pkgset_path				    = os.path.join(config_path, 'package.sets')
portage_frags_path	        = os.path.join(config_path, 'portage.frags')
buildhook_frags_path	    = os.path.join(config_path, 'buildhook.frags')
kconf_frags_path            = os.path.join(config_path, 'kconf.frags')
patch_diff_path		        = os.path.join(config_path, 'patch.diffs')
patch_profiles_path         = os.path.join(config_path, 'patch.profiles')
# Environment settings (ie: Stuff you set and forget.)
config_env_path             = os.path.join(config_path, 'env')
config_arch_path		    = os.path.join(config_env_path, 'arch')
# These pertain to the stage signing.
asc_ext			            = '.DIGESTS.asc'
gentoo_signing_key		    = "0xBB572E0E2D182910"
gentoo_upstream_url         = "http://ftp-osl.osuosl.org/pub/gentoo/releases/"
# These are the base profiles we download from upstream. Gentoomuch recompiles these with architecture-optmized flags and further build upon the results.
profiles_amd64			    = ('default', 'hardened+nomultilib', 'hardened-selinux+nomultilib', 'hardened-selinux', 'hardened', 'musl-hardened', 'musl-vanilla', 'nomultilib', 'systemd', 'uclibc-hardened', 'uclibc-vanilla', 'x32')
# This is for the Docker tags that we access as we work.
profiles_amd64_dockerized   =  ( get_dockerized_profile_name(p) for p in profiles_amd64 )
image_tag_base		   	    = 'localhost:5000/gentoomodern-'
active_image_tag            = image_tag_base + 'current:latest'
dockerized_username         = 'gentoomodern-user'
usage_str                   = "    gentoomodern "
# Patches
ebuilds_export_mountpoint   = '/home/' + dockerized_username + '/ebuild_exports'
