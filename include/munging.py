#!/usr/bin/env python3

import sys, os, re
from typing import Dict, List, Set

debug = False

stage_parts = ('cpu', 'packages', 'flags', 'profile')
dont_munge_files = ('bashrc', 'modules')
dont_munge_dirs = ('sets', 'patches')

msg_prefix           = '[Zentoo.munging] '
config_dir           = './config/'
stage_path           = config_dir + 'stage.defines'
cpu_path             = config_dir + 'cpu.defines'
pkgset_path          = config_dir + 'package.sets'
flagset_path         = config_dir + 'portage.locals'
hooks_path           = config_dir + 'build.hooks'
kernel_path         = config_dir + 'kernel.defines'
default_flags_path           = config_dir + 'portage.global'
flags_include_path   = './include/portage.defaults'

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
def get_flagname(flag_str):
    return re.sub('^(-)+', '', flag_str)

def get_flagname_test():
    if not get_flagname('silly-thing/dontchangeme') == 'silly-thing/dontchangeme':
        sys.exit("Failed get_flagname test: Should not change flags' contents.")
    if not get_flagname('-silly-thing/testme') == 'silly-thing/testme':
        sys.exit('Failed get_flagname test: Single neg.')
    if not get_flagname('--silly-thing/testmemore') == 'silly-thing/testmemore':
        sys.exit('Failed get_flagname test: Multiple negative signs.')
    if not get_flagname('-') == '':
        sys.exit('Failed get_flagname test: Empty flag.')

# This deduplicates keywords and verifies for set/unset combinations.
def ingest_conf(file_content_list, variables_to_flags: Dict[str, Dict[bool, List[str]]]):
    for line in file_content_list:
        if not re.match('(\S)+', line): # Only proceed if we have an empty line... Those make the regex crash
            continue
        if debug:
            print('ZENTOO DEBUG - line: ' + line)
        line = re.sub('(=|\'|")+', ' ', line) # Strip out troublesome characters
        variable_name = re.match('^\S+', line).group()
        if variable_name[0] == '#': # Skip comments
            continue
        if debug:
            print('ZENTOO DEBUG - line (cleaned): ' + line)
            print('ZENTOO DEBUG - variable name: ' + variable_name)
        flags_str = re.sub('^' + re.escape(variable_name), '', line)
        if debug:
            print('ZENTOO DEBUG - flags string: ' + flags_str)
        if not variable_name in variables_to_flags:
            variables_to_flags[variable_name] = dict()
        if True not in variables_to_flags[variable_name]:
            variables_to_flags[variable_name][True] = dict()
            variables_to_flags[variable_name][True] = []
        if False not in variables_to_flags[variable_name]:
            variables_to_flags[variable_name][False] = dict()
            variables_to_flags[variable_name][False] = []
        is_setting = False
        for candidate_flag in flags_str.split():
            if not candidate_flag.strip() == '':
                if debug:
                    print('Examining flag ' + candidate_flag)
                flag_abs = get_flagname(candidate_flag)
                if flag_abs == candidate_flag:
                    is_setting = True
                else:
                    is_setting = False
                if is_setting:
                    if flag_abs in variables_to_flags[variable_name][True]:
                        continue
                    elif flag_abs in variables_to_flags[variable_name][False]:
                        return False
                    else:
                        variables_to_flags[variable_name][True].append(flag_abs)
                if not is_setting:
                    if flag_abs in variables_to_flags[variable_name][True]:
                        return False
                    elif flag_abs in variables_to_flags[variable_name][False]:
                        continue
                    else:
                        variables_to_flags[variable_name][False].append(flag_abs)
    return True


# Determine equivalence partitions.
def ingest_conf_test():
    desired = { 'AB': { True: ['nice-enough'], False: ['awful'] } }
    results = dict()
    test_1 = ['AB=\'-awful nice-enough\'', 'AB=-awful']
    if not ingest_conf(test_1, results):
        sys.exit('Failed ingest_conf: testset1. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_conf: testset1. Bad results.')
    test_2 = ['AB = -awful nice-enough -awful']
    if not ingest_conf(test_2, results):
        sys.exit('Failed ingest_conf: testset2. Should return true.')
    if not results == desired:
       sys.exit('Failed ingest_conf: testset2. Bad results.')
    test_3 = ['AB="-awful nice-enough awful"']
    if ingest_conf(test_3, results):
        sys.exit('Failed ingest_conf: testset3 (yes and no). Should return false.')
    if not results == desired:
        sys.exit('Failed ingest_conf: testset3 (yes and no). Bad results.')
    test_4 = ["AB='nice-enough -awful nice-enough'", "AB=' nice-enough'"]
    if not ingest_conf(test_4, results):
        sys.exit('Failed ingest_conf: testset4. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_conf: testset4. Bad results.')


# Ok, this is gonna be fun...
# First (string) key represents the filename
# Second (string) key is the variable/package atom
# Third (bool) key is whether or not the flags (up next) is off or on
# Our flags are held in a list: Depending on whether or not there is a negative sign in-front, a flag is found in a list referenced by the key of True or False. For variables with flags such as -march=..., it will be interpreted as a negative, so you must drain both lists.
def collect_portage_vars(config_dir, config_name, portage_environment : Dict[str, Dict[str, Dict[bool, List[str]]]]):
    for (dirpath, dirnames, filenames) in os.walk(config_dir):
        print('Walking over ' + dirpath)
        for f in filenames:
            if not f in dont_munge_files and not dirpath in dont_munge_dirs:
                print('Ingesting ' + f)
                lines = read_file_lines(dirpath + '/' + f)
                # We need to strip the global directory information in order to have the (local) config filenames all indexing into their proper key. This means lots of nested regexps. Huh.
                cleaned_filename = re.sub(re.escape(flags_include_path),  '', f)
                cleaned_filename = re.sub(re.escape(default_flags_path),  '', cleaned_filename)
                cleaned_filename = re.sub(re.escape(flagset_path)      ,  '', cleaned_filename)
                cleaned_filename = re.sub(re.escape(cpu_path)          ,  '', cleaned_filename)
                cleaned_filename = re.sub('^' + re.escape(config_name) ,  '', cleaned_filename)
                cleaned_filename = re.sub('^/'                         ,  '', cleaned_filename)
                if not cleaned_filename == '': # Blank names mess things up.
                    if cleaned_filename in portage_environment:
                        ingest_conf(lines, portage_environment[cleaned_filename])
                    else:
                        portage_environment[cleaned_filename] = dict()
                        ingest_conf(lines, portage_environment[cleaned_filename])
            print('Done ingesting ' + cleaned_filename)


# This deals with the setup, copying, and file-munging needed to transform a cpu config and a user flags config into our ./work/portage directory
# If no arguments are provided, it will simply use the default (blank, unoptimized) configuration with no packages.
# Here, we do not munge anything under 
def checkout_config(cpu_conf = 'zentoo/default', flags_conf : List[str] = []):
    custom_cpu = False
    custom_flags = False
    # Verify existence of directories
    if debug:
        print('Checking portage includes')
    if not os.path.isdir(flags_include_path):
        print('Global (immutable, site-wide) Portage/flags config directory at ' + flags_include_path + ' does not exist.')
        return False
    if debug:
        print('Checking portage globals')
    if not os.path.isdir(default_flags_path):
        print('Global (user-defined) Portage/flags config directory at ' + default_flags_path + ' does not exist.')
        return False
    if not cpu_conf == '':
        if os.path.isdir(cpu_path + '/' + cpu_conf):
            custom_cpu = True
        else:
            print('The user-provided CPU config directory at ' + cpu_path + '/' + cpu_conf + ' does not exist.')
            return False
    if debug:
        print('Checking for the existence of local flagsets')
    if len(flags_conf) > 0:
        for flg in flags_conf:
            flg = flg.strip()
            if flg == '':
                continue
            if os.path.isdir(flagset_path + '/' + flg):
                custom_flags = True
            else:
                print('The user-provided local Portage/flags directory at ' + flagset_path + '/' + flgs  + ' does not exist.')
                return False
    if debug:
        print('Setting up work env')
    sync_patches_str = ''
    if os.path.isdir(flagset_path + '/patches'):
        sync_patches_str += ' && rsync -aHXqv ' + flagset_path + '/patches/* ./work/portage/patches'
    if os.path.isdir(default_flags_path + '/patches'):
        sync_patches_str += ' && rsync -aHVqv ' + default_flags_path + '/' + flags_conf + '/patches/* ./work/portage/patches'
    code = os.system('mkdir -p ./work/portage/sets && mkdir -p ./work/portage/patches && rsync -aHXqv ./config/package.sets/* ./work/portage/sets ' + sync_patches_str)
    if not code == 0:
        return False
    for d in (flagset_path, default_flags_path, flags_include_path):
        code = os.system('cp ' + d + '/bashrc work/portage')
        if code == 0: ## To ensure the operation happens in-line with the rest of the script
            continue
    portage_vars = dict()
    collect_portage_vars(flags_include_path, '', portage_vars)
    collect_portage_vars(default_flags_path, '', portage_vars)
    if custom_cpu:
        collect_portage_vars(cpu_path + '/' + cpu_conf, cpu_conf, portage_vars)
    if custom_flags:
        for line in flags_conf:
            for token in line.split():
                token = token.strip()
                if len(token) > 0:
                    collect_portage_vars(flagset_path + '/' + token, token, portage_vars)

    for filepath in portage_vars:
        if debug:
            print('File ' + filepath)
        expanded_filepath = filepath.split('/')
        if debug:
            print(expanded_filepath)
            print('Expanded filepath (list) length = ' + str(len(expanded_filepath)))
        prefix = './work/portage/'
        if len(expanded_filepath) > 1:
            if debug:
                print('Going into deeper waters')
            for p in expanded_filepath[:-1]:
                prefix += p
                prefix += '/'
                if debug:
                    print('prefix = ' + prefix)
                if not os.path.isdir(prefix):
                    if debug:
                        print('Making directory ' + prefix)
                    os.mkdir(prefix)
        lines = []
        filename = ''
        if len(expanded_filepath) > 1:
            filename = expanded_filepath[-1]
        else:
            filename = filepath
        uses_equals_sign = False
        if filename[-5:] == '.conf':
            uses_equals_sign = True
        for variable in portage_vars[filepath]:
            current_line = variable
            if uses_equals_sign:
                current_line += '='
            current_line += ' '
            counter = 1
            for flag in portage_vars[filepath][variable][True]:
                current_line += flag
                if counter < len(portage_vars[filepath]):
                    current_line += ' '
                counter += 1
            counter = 1
            for flag in portage_vars[filepath][variable][False]:
                current_line += '-'
                current_line += flag
                if counter < len(portage_vars[filepath]):
                    current_line += ' '
                counter += 1
            current_line += '\n'
            lines.append(current_line)
        write_file_lines(prefix + filename, lines)
    return True


# This will ensure that user-defined sets of Portage configurations listed in a subdirectory of ./config/stage.defines/ actually all exist! 
def check_if_portage_sets_present(portage_sets : List[str]):
    for line in portage_sets:
        for token in line.split():
            token = token.strip()
            if len(token) > 0:
                if token[0] == '@':
                    token = token[2:]
            if not os.path.isdir(flagset_path + '/' + token):
                print(msg_prefix + 'Local portage directory not found: ' + flagset_path + token + ', while seeking out attached sets.')
                return False
    return True


# This turns a stage.defines config into a ./work/portage directory
# The second argument represents things that the caller needs to run afterwards.
def stage3_config(user_stage, todo : Dict[str, List[str]]):
    os.system('rm -rf ./work/portage/*')
    user_stage_path = stage_path + '/' + user_stage
    if not os.path.isdir(user_stage_path):
        print(msg_prefix + 'Could not find stage definitions directory: ' + user_stage_path)
        return False
    if os.path.isfile(user_stage_path + '/cpu'):
        cpu_conf = open(user_stage_path + '/cpu').read().strip()
        if not os.path.isdir(cpu_path + '/' + cpu_conf):
            print(msg_prefix + 'CPU config directory: ' + cpu_path + '/' + cpu_conf + ' does not exist.')
            return False
    if os.path.isfile(user_stage_path + '/flags'):
        flags_conf = open(user_stage_path + '/flags').read().split()
        if not check_if_portage_sets_present(flags_conf):
            print('Could not find all attached flagsets')
            return False
    if os.path.isfile(user_stage_path + '/packages'):
        todo['packages'] = read_file_lines(user_stage_path + '/packages')
    if os.path.isfile(user_stage_path + '/profiles'):
        todo['profiles'] = read_file_lines(user_stage_path + '/profiles')
    if os.path.isfile(user_stage_path + '/hooks'):
        todo['hooks'] = read_file_lines(user_stage_path + '/hooks')
    code = checkout_config(cpu_conf, flags_conf)
    if code == False:
        print('Checkout config failed')
        return False
    return True
