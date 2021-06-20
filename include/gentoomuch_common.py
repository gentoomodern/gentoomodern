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
# Config defines
config_path				    		= './config'
stage_defines_path		    		= os.path.join(config_path, 'stage.defines')
kernel_defines_path            		= os.path.join(config_path, 'kernel.defines')
cpu_path				    		= os.path.join(config_path, 'cpu.defines')
pkgset_path				    		= os.path.join(config_path, 'package.sets')
local_config_basepath	       		= os.path.join(config_path, 'portage.frags')
hooks_path				       		= os.path.join(config_path, 'build.hooks')
kconf_frags_path				    = os.path.join(config_path, 'kconf.frags')
saved_patches_path		       		= os.path.join(config_path, 'user.patches')
topatch_config_path            		= os.path.join(config_path, 'patches.apply')
# Environment settings (ie: Stuff you set and forget.)
env_settings_path              		= os.path.join(config_path, 'env')
arch_config_path		       		= os.path.join(env_settings_path, 'arch')
# These pertain to the stage signing.
asc_ext			               		= '.DIGESTS.asc'
gentoo_signing_key		       		= "0xBB572E0E2D182910"
gentoo_upstream_url            		= "http://ftp-osl.osuosl.org/pub/gentoo/releases/"
# These are the base profiles we download from upstream. Gentoomuch recompiles these with architecture-optmized flags and further build upon the results.
profiles_amd64			       		= ('default','hardened+nomultilib','hardened-selinux+nomultilib','hardened-selinux','hardened','musl-hardened','musl-vanilla','nomultilib','systemd','uclibc-hardened','uclibc-vanilla','x32')
# This is for the Docker tags that we access as we work.
image_tag_base			       		= 'localhost:5000/gentoomuch-'
active_image_tag		       		= image_tag_base + 'current:latest'
profiles_amd64_dockerized	   		=  ( get_dockerized_profile_name(p) for p in profiles_amd64 )
dockerized_username            		= 'gentoomuch-user'
usage_str                      		= "    gentoomuch "
# Patches
patches_mountpoint             		= '/home/' + dockerized_username + '/ebuild_exports'
