#!/usr/bin/env python3

import re

# Stuff all scripts here should use
debug = True
output_path                 = './work/'
stages_path                 = output_path + 'stages/'
portage_output_path         = output_path + 'portage/'
current_stage_path	    = output_path + 'current_stage'
current_profile_path	    = output_path + 'current_profile'
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


#def get_sed_str_upstream(arch, profile):
#    return "sed 's/.*    PS1.*/    PS1=\"\u@ " + arch + '-' + profile + "-upstream\"/ "

#def get_sed_str(arch, profile, stage):
#    return "sed 's/.*    PS1.*/    PS1=\"\u@ " + arch + '-' + profile + '-' + stage  + "\"/ "

profiles_amd64 = ( 'default', 'hardened+nomultilib', 'hardened-selinux+nomultilib', 'hardened-selinux', 'hardened', 'musl-hardened', 'musl-vanilla', 'nomultilib', 'systemd', 'uclibc-hardened', 'uclibc-vanilla', 'x32' )


def get_cleaned_profile(profile):
    return re.sub(re.escape('+'), '-', profile) # Found that one out when working with musl+selinux...

profiles_amd64_cleaned = { get_cleaned_profile(p) for p in profiles_amd64 }

# TODO: Move these convenience functions
def read_file_lines(filename):
    f = open(filename)
    lines = f.readlines()
    return lines

def write_file_lines(filename, lines, uid = -1, gid = -1):
    f = open(filename, 'w')
    f.writelines(lines)
    f.close()
    if uid > 0:
        if gid < 0:
            os.chown(filename, uid, uid)
        else:
            os.chown(filename, uid, gid)

# https://stackoverflow.com/questions/16402525/python-read-whitespace-separated-strings-from-file-similar-to-readline
def read_by_tokens(obj):
    for line in obj:
        for token in line.split():
            yield token

# TODO: Write a test or two
def get_cleaned_path(dirpath, local_config_path):
    results = dirpath
    results = re.sub(re.escape(local_config_path)           , '', results)
    results = re.sub(re.escape(portage_output_path)         , '', results)
    results = re.sub(re.escape(global_config_path)          , '', results)
    results = re.sub(re.escape(local_config_basepath)       , '', results)
    results = re.sub(re.escape(cpu_path)                    , '', results)
    results = re.sub('^/'                                   , '', results)
    return results

#def get_cleaned_stagedef(stage_define):
#	return re.sub('/', '\/', stage_define) # / gets intepreted as a repository in docker, so fix that up.
