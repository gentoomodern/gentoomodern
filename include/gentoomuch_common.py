#!/usr/bin/env python3

import re, os
from .get_dockerized_profile_name import get_dockerized_profile_name


#Stuff all scripts here should use
debug				        		= True
output_path				    		= './gentoomuch-data'
stages_path		            		= os.path.join(output_path, 'stages')
gpg_path				    		= os.path.join(output_path, 'gpg')
squashed_path                  		= os.path.join(output_path, 'squashed')
emergelogs_path             		= os.path.join(output_path, 'emerge.logs')
patches_workdir                		= os.path.join(output_path, 'patches')
env_output_path                		= os.path.join(output_path, 'env')
desired_stage_path		    		= os.path.join(env_output_path, 'desired_stage')
desired_profile_path	    		= os.path.join(env_output_path, 'desired_profile')
desired_packages_path	    		= os.path.join(env_output_path, 'desired_packages')
desired_hooks_path		    		= os.path.join(env_output_path, 'desired_hooks')
patches_in_progress_dir        		= os.path.join(env_output_path, 'patches')
# Portage-related
portage_output_path		    		= os.path.join(output_path, 'portage')
sets_output_path		    		= os.path.join(portage_output_path, 'sets')
patches_output_path            		= os.path.join(portage_output_path, 'patches')
# Includes (immutable data)
includes_path			    		= './include'
global_portage_config_path		    = os.path.join(includes_path, 'portage.global')
dockerfiles_path		    		= os.path.join(includes_path, 'dockerfiles')
# Config defines, local
local_config_path				    = './config/local'
local_stage_defines_path		    = os.path.join(local_config_path, 'stage.defines')
local_kernel_defines_path           = os.path.join(local_config_path, 'kernel.defines')
local_system_defines_path           = os.path.join(local_config_path, 'system.defines')
local_buildhook_defines_path	    = os.path.join(local_config_path, 'buildhook.defines')
local_cpu_frags_path				= os.path.join(local_config_path, 'cpu.frags')
local_pkgset_path				    = os.path.join(local_config_path, 'package.sets')
local_portage_frags_path	       	= os.path.join(local_config_path, 'portage.frags')
local_buildhook_frags_path	        = os.path.join(local_config_path, 'buildhook.frags')
local_kconf_frags_path	            = os.path.join(local_config_path, 'kconf.frags')
local_patch_diff_path		        = os.path.join(local_config_path, 'patch.diffs')
local_patch_profiles_path           = os.path.join(local_config_path, 'patch.profiles')
# Environment settings (ie: Stuff you set and forget.)
local_config_env_path              	= os.path.join(local_config_path, 'env')
local_config_arch_path		       	= os.path.join(local_config_env_path, 'arch')
# Config defines, included
included_config_path                = "./config/include"
included_stage_defines_path		    = os.path.join(included_config_path, 'stage.defines')
included_kernel_defines_path        = os.path.join(included_config_path, 'kernel.defines')
included_system_defines_path        = os.path.join(included_config_path, 'system.defines')
included_buildhook_defines_path	    = os.path.join(included_config_path, 'buildhook.defines')
included_cpu_frags_path				= os.path.join(included_config_path, 'cpu.frags')
included_pkgset_path				= os.path.join(included_config_path, 'package.sets')
included_portage_frags_path	       	= os.path.join(included_config_path, 'portage.frags')
included_buildhook_frags_path	    = os.path.join(included_config_path, 'buildhook.frags')
included_kconf_frags_path	        = os.path.join(included_config_path, 'kconf.frags')
included_patch_diff_path		    = os.path.join(included_config_path, 'patch.diffs')
included_patch_profiles_path        = os.path.join(included_config_path, 'patch.profiles')
# These pertain to the stage signing.
asc_ext			               		= '.DIGESTS.asc'
gentoo_signing_key		       		= "0xBB572E0E2D182910"
gentoo_upstream_url            		= "http://ftp-osl.osuosl.org/pub/gentoo/releases/"
# These are the base profiles we download from upstream. Gentoomuch recompiles these with architecture-optmized flags and further build upon the results.
profiles_amd64			       		= ('default','hardened+nomultilib','hardened-selinux+nomultilib','hardened-selinux','hardened','musl-hardened','musl-vanilla','nomultilib','systemd','uclibc-hardened','uclibc-vanilla','x32')
# This is for the Docker tags that we access as we work.
profiles_amd64_dockerized	   		=  ( get_dockerized_profile_name(p) for p in profiles_amd64 )
image_tag_base			       		= 'localhost:5000/gentoomuch-'
active_image_tag		       		= image_tag_base + 'current:latest'
dockerized_username            		= 'gentoomuch-user'
usage_str                      		= "    gentoomuch "
# Patches
ebuilds_export_mountpoint           = '/home/' + dockerized_username + '/ebuild_exports'
