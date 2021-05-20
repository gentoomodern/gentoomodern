#!/usr/bin/env python3

import re

# Stuff all scripts here should use
debug = True
output_path                 = './work/'
portage_output_path         = output_path + 'portage/'
includes_path               = './include/'
global_config_path          = includes_path + 'portage.global/'
config_path                 = './config/'
stage_defines_path          = config_path + 'stage.defines/'
cpu_path                    = config_path + 'cpu.defines/'
pkgset_path                 = config_path + 'package.sets/'
patches_path                = config_path + 'patches/'
local_config_basepath       = config_path + 'portage.locals/'
hooks_path                  = config_path + 'build.hooks/'
kernel_path                 = config_path + 'kernel.defines/'
arch_config_path            = config_path + 'arch'
current_basestage_path      = config_path + 'base-stage'
current_portage_path        = config_path + 'user-stage'

sets_output_path = './work/portage/sets'
patches_output_path = './work/portage/patches'

# TODO: Move these convenience functions
def read_file_lines(filename):
    f = open(filename)
    lines = f.readlines()
    return lines

def write_file_lines(filename, lines):
    f = open(filename, 'w')
    f.writelines(lines)
    f.close()

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
