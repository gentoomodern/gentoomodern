#!/usr/bin/envpython3

import re
from .get_dockerized_profile_name import get_dockerized_profile_name


#Stuff all scripts here should use
debug				        =	True
output_path				    =	'./gentoomuch-data/'
stages_path		            =	output_path + 'stages/'
gpg_path				    =   output_path + 'gpg/'
emergelogs_path             =   output_path + 'emerge.logs/'
desired_stage_path		    =   output_path + 'desired_stage'
desired_profile_path	    =	output_path + 'desired_profile'
desired_packages_path	    =	output_path + 'desired_packages'
desired_hooks_path		    =	output_path + 'desired_hooks'
# Portage-related
portage_output_path		    =	output_path + 'portage/'
sets_output_path		    =  	portage_output_path + 'sets/'
patches_output_path 	    =	portage_output_path + 'patches/'
# Includes (immutable data)
includes_path			    =   './include/'
global_config_path		    =	includes_path + 'portage.global/'
dockerfiles_path		    =   includes_path + 'dockerfiles/'
# Config defines
config_path				    =   './config/'
stage_defines_path		    =   config_path + 'stage.defines/'
cpu_path				    =   config_path + 'cpu.defines/'
pkgset_path				    =   config_path + 'package.sets/'
patches_path			    =   config_path + 'user.patches/'
local_config_basepath	    =   config_path + 'portage.locals/'
hooks_path				    =   config_path + 'build.hooks/'
kernel_path				    =   config_path + 'kernel.defines/'
arch_config_path		    =   config_path + 'arch'
uid_config_path			    =   config_path + 'uid'
# The follow file seed not necessarily exist; only for custom deployments with specific permission needs..
gid_config_path			    =   config_path + 'gid'
# These pertain to the stage signing.
asc_ext			            =   '.DIGESTS.asc'
gentoo_signing_key		    =	"0xBB572E0E2D182910"
gentoo_upstream_url         =	"http://ftp-osl.osuosl.org/pub/gentoo/releases/"
# These are the base profiles we download from upstream. Gentoomuch recompiles these with architecture-optmized flags and further build upon the results.
profiles_amd64			    =	('default','hardened+nomultilib','hardened-selinux+nomultilib','hardened-selinux','hardened','musl-hardened','musl-vanilla','nomultilib','systemd','uclibc-hardened','uclibc-vanilla','x32')
# This is for the Docker tags that we access as we work.
image_tag_base			    =	'localhost:5000/gentoomuch-'
active_image_tag		    =	image_tag_base + 'current:latest'
profiles_amd64_dockerized	=   ( get_dockerized_profile_name(p) for p in profiles_amd64 )
