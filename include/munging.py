#!/usr/bin/env python3

import sys, os, re
from typing import Dict, List, Set

stage_parts = ('cpu', 'packages', 'flags', 'profile')
dont_munge_pkgflag_files = ('bashrc', 'modules', 'README.md')
dont_munge_pkgflag_dirs = ('sets', 'patches')

output_path        = './work/portage/'
msg_prefix         = '[Zentoo.munging] '
config_dir         = './config/'
stage_path         = config_dir + 'stage.defines/'
cpu_path           = config_dir + 'cpu.defines/'
pkgset_path        = config_dir + 'package.sets/'
flagset_path       = config_dir + 'portage.locals/'
hooks_path         = config_dir + 'build.hooks/'
kernel_path        = config_dir + 'kernel.defines/'
global_flags_path = config_dir + 'portage.global/'
flags_include_path = './include/portage.defaults/'




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


# This deduplicates keywords within a single file, given as a list of strings (newline-separated.)
# It will verify for set/unset combinations and return False upon spotting one.
# This allows the user to avoid potential surprises.
def ingest_pkgflag_config(file_content_list, package_atoms_to_flags: Dict[str, Dict[bool, List[str]]], target_packages : Set[str] = [], debug = False):
    for line in file_content_list:
        if not re.match('(\S)+', line): # Only proceed if we don't have an empty line... Those make the regex engine crash
            continue
        if debug:
            print('ZENTOO DEBUG - line: ' + line)
        line = re.sub('(\'|")+', '', line) # Strip out troublesome characters
        pkg_name = re.match('^\S+', line).group() # Get the first block of non-whitespace characters
        if pkg_name[0] == '#': # Skip comments
            continue
        if len(target_packages) > 0:
            if not pkg_name in target_packages: # Ensure we only ingest the variables we desire to take; some files have different formats within themselves. :(
                continue
        flags_str = re.sub('^' + re.escape(pkg_name), '', line)
        if debug:
            print('ZENTOO DEBUG - line (cleaned): ' + line)
            print('ZENTOO DEBUG - variable name: ' + pkg_name)
            print('ZENTOO DEBUG - flags string: ' + flags_str)
        if not pkg_name in package_atoms_to_flags: # Initialize if necessary   
            package_atoms_to_flags[pkg_name] = dict() 
        if True not in package_atoms_to_flags[pkg_name]: # Initialize if necessary
            package_atoms_to_flags[pkg_name][True] = []
        if False not in package_atoms_to_flags[pkg_name]: # Initialize if necessary
            package_atoms_to_flags[pkg_name][False] = []
        for candidate_flag in flags_str.split():
            if not candidate_flag.strip() == '': # Ensure we actually have text to work with
                if debug:
                    print('Examining flag ' + candidate_flag)
                flag_abs = get_flagname(candidate_flag) # We give our flag its absolute value
                if candidate_flag[0] == '#': # An equals sign is not a flag.
                    continue
                if flag_abs == candidate_flag: # Are we setting or unsetting? We determine that by stripping out the - sign and asking ourselves whether it gives us the same input flag
                    is_setting = True
                if len(candidate_flag) == 0:
                    continue
                if candidate_flag == '=':
                    continue
                else:
                    is_setting = False
                is_setting_inverse = not is_setting
                if flag_abs in package_atoms_to_flags[pkg_name][is_setting]: # If it's already in our list, we can move on. That's how we implement deduplication!
                    continue
                elif flag_abs in package_atoms_to_flags[pkg_name][is_setting_inverse]: # If that flag is in the list for negatives, then adding a positive flag will only cause confusion.
                    return False
                else:
                    package_atoms_to_flags[pkg_name][is_setting].append(flag_abs) # We now can append anything that has passed the previous tests.
    return True


# Determine equivalence partitions.
def ingest_pkgflag_config_test():
    desired = { 'AB': { True: ['nice-enough'], False: ['awful'] } }
    results = dict()
    test_1 = ['AB=\'-awful nice-enough\'', 'AB=-awful']
    if not ingest_pkgflag_config(test_1, results):
        sys.exit('Failed ingest_pkgflag_config: testset1. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_pkgflag_config: testset1. Bad results.')
    test_2 = ['AB = -awful nice-enough -awful']
    if not ingest_pkgflag_config(test_2, results):
        sys.exit('Failed ingest_pkgflag_config: testset2. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_pkgflag_config: testset2. Bad results.')
    test_3 = ['AB="-awful nice-enough awful"']
    if ingest_pkgflag_config(test_3, results):
         sys.exit('Failed ingest_pkgflag_config: testset3 (yes and no). Should return false.')
    if not results == desired:
        sys.exit('Failed ingest_pkgflag_config: testset3 (yes and no). Bad results.')
    test_4 = ["AB='nice-enough -awful nice-enough'", "AB=' nice-enough'"]
    if not ingest_pkgflag_config(test_4, results):
        sys.exit('Failed ingest_pkgflag_config: testset4. Should return true.')
    if not results == desired:
        sys.exit('Failed ingest_pkgflag_config: testset4. Bad results.')


def ingest_makefile_config(file_content_list, variables_to_flags: Dict[str, List[str]], target_variables : Set[str] = (), debug = False):
    for line in file_content_list:
        if not re.match('(\S)+', line): # Only proceed if we don't have an empty line... Those make the regex engine crash
            continue
        if debug:
            print('ZENTOO DEBUG - line: ' + line)
        line = re.sub('(\'|")+', '', line) # Strip out troublesome characters
        variable_name = re.match('^(\S)+', line).group() # Get the first block of non-whitespace characters
        if variable_name[0] == '#': # Skip comments
            continue
        #variable_name = re.sub('=', ' ', variable_name)
        #variable_name = variable_name.split()[0]#.strip()#re.match('^(\S)+', '', variable_name).group()
        #if variable_name[len(variable_name)] == '=': # Remove the = Sign from the variable name: TODO: Is that even necessary??
        #    variable_name = variable_name[:-1]
        if len(target_variables) > 0: # If we give an empty set of target variables, we scoop 'em all!
            if not variable_name in target_variables: # Ensure we only ingest the variables we desire to take; some files have different formats within themselves. :(
                continue
        flags_str = re.sub('^' + re.escape(variable_name), ' ', line)
        if debug:
            print('ZENTOO DEBUG - line (cleaned): ' + line)
            print('ZENTOO DEBUG - variable name: ' + variable_name)
            print('ZENTOO DEBUG - flags string: ' + flags_str)
        if not variable_name in variables_to_flags: # Initialize if necessary   
            variables_to_flags[variable_name] = dict() 
            variables_to_flags[variable_name] = []
        for candidate_flag in flags_str.split():
            if not candidate_flag.strip() == '': # Ensure we actually have text to work with
                if debug:
                    print('Examining flag ' + candidate_flag)
                if candidate_flag[0] == '#': # Stop the line at comments
                    break
                if candidate_flag == '':
                    continue
                if candidate_flag[0] == '=':
                    candidate_flag = candidate_flag[2:]
                if candidate_flag in variables_to_flags[variable_name]: # IF already present
                    continue
                else:
                    variables_to_flags[variable_name].append(candidate_flag) # We can append, now.
    return True


def get_cleaned_dirpath(dirpath, config_path, config_name):
    results = re.sub(re.escape(flags_include_path)       , '', dirpath)
    results = re.sub(re.escape(global_flags_path)        , '', results)
    results = re.sub(re.escape(flagset_path)             , '', results)
    results = re.sub(re.escape(cpu_path)                 , '', results)
    results = re.sub(re.escape(config_path)              , '', results)
    results = re.sub(re.escape(config_name)              , '', results)
    results = re.sub('^/'                                , '', results)
    return results


# Ok, this is gonna be fun...
# First (string) key represents the filename
# Second (string) key is the variable/package atom
# Third (bool) key is whether or not the flags (up next) is off or on
# Our flags are held in a list: Depending on whether or not there is a negative sign in-front, a flag is found in a list referenced by the key of True or False.
def collect_package_flags(local_config_dir, local_config_name, package_flags_environment : Dict[str, Dict[str, Dict[bool, List[str]]]], debug = False):
    for (dirpath, dirnames, filenames) in os.walk(local_config_dir):
        print('Walking over ' + dirpath + ' With local config name ' + local_config_name)
        cleaned_dirpath = get_cleaned_dirpath(dirpath, local_config_dir, local_config_name)
        print('Walking over (cleaned) ' + cleaned_dirpath)
        if cleaned_dirpath in dont_munge_pkgflag_dirs:
            continue
        for f in filenames:
            if f in dont_munge_pkgflag_files:
                continue
            if debug:
                print('Ingesting ' + f)
            cleaned_filepath = cleaned_dirpath + '/' + f
            if cleaned_filepath[0] == '/':
                cleaned_filepath = cleaned_filepath[1:]
            print('Filepath: ' + f + ', Filepath (cleaned): ' + cleaned_filepath)
            lines = read_file_lines(dirpath + '/' + f)
           # We need to strip the global directory information in order to have the (local) config filenames all indexing into their proper key. This means lots of nested regexps. Huh.
            if not cleaned_filepath == '': # Blank names mess things up.
                if cleaned_filepath in package_flags_environment:
                    ingest_pkgflag_config(lines, package_flags_environment[cleaned_filepath])
                else:
                    package_flags_environment[cleaned_filepath] = dict()
                    ingest_pkgflag_config(lines, package_flags_environment[cleaned_filepath])
            if debug:
                print('Done ingesting ' + cleaned_filepath)
    return True


# This function acts a bit differently in manner than the one collecting package flags.
# The handling is far simpler: We strip out parentheses and keep our negative signs.
def collect_portage_vars(local_config_dir, local_config_name, portage_conf_environment: Dict[str, Dict[str, List[str]]], debug = False):
    for (dirpath, dirnames, filenames) in os.walk(local_config_dir):
        cleaned_dirpath = get_cleaned_dirpath(dirpath, local_config_dir, local_config_name)
        print('Walking over ' + dirpath + ' With local config name ' + local_config_name)
        print('Walking over (cleaned) ' + cleaned_dirpath)
        if cleaned_dirpath in dont_munge_pkgflag_dirs:
            continue
        for f in filenames:
            if f in dont_munge_pkgflag_files:
                continue
            cleaned_filepath = cleaned_dirpath + '/' + f
            if cleaned_filepath[0] == '/':
                cleaned_filepath = cleaned_filepath[1:]
            print('Filepath: ' + f + ', Filepath (cleaned): ' + cleaned_filepath)
            lines = read_file_lines(dirpath + '/' + f)
            # We need to strip the global directory information in order to have the (local) config filenames all indexing into their proper key. This means lots of nested regexps. Huh.
            if not cleaned_filepath == '': # Blank names mess things up.
                if cleaned_filepath in portage_conf_environment:
                    ingest_makefile_config(lines, portage_conf_environment[cleaned_filepath])
                else:
                    portage_conf_environment[cleaned_filepath] = dict()
                    ingest_makefile_config(lines, portage_conf_environment[cleaned_filepath])
            if debug:
                print('Done ingesting ' + cleaned_filepath)
    return True


# In this, we create all the folders necessary to recreate our desired portage filestructure.
def create_output_directory_structure(filepaths : List[str], debug = False):
    for fpath in filepaths: 
        if debug:
            print('File ' + fpath)
        expanded_fpath = fpath.split('/')
        if debug:
            print(expanded_fpath)
            print('Expanded fpath (list) length = ' + str(len(expanded_fpath)))
        prefix = output_path
        if len(expanded_fpath) > 1: # If we're still considering a directory and not a file
            if debug:
                print('Going deeper into the filestructure') # TODO: Make more sense
            for p in expanded_fpath[:-1]: # The last element is the filename itself
                prefix += '/'
                prefix += p
                if debug:
                    print('prefix = ' + prefix)
                if not os.path.isdir(prefix):
                    if debug:
                        print('Making directory ' + prefix)
                    os.mkdir(prefix) # Now we finally make our directory. Is there a better way to do this???


# This returns a dictionary containing the file paths. Each has its contents stored in a list of strings, one for each line.
def recreate_output_files(portage_conf_environment : Dict[str, Dict[str, List[str]]], package_flags_environment : Dict[str, Dict[str, Dict[bool, List[str]]]], debug = False):
    results = dict()
    # Output all the content of the conf files
    # TODO: Ensure that variables referred in later invocations get added prior to the ones that refer them. We'll need to use some form of topo sort, either implicitly or explicitly.
    for f in portage_conf_environment:
        results[f] = []
        for v in portage_conf_environment[f]:
            line = v
            line += '= "'
            # counter = 1
            for token in portage_conf_environment[f][v]:
                line += token
                # if counter < len(portage_conf_environment[f][v]):
                line += ' '
                # counter += 1
            line += '"'
            results[f].append(line)
    # Now, output all the flag-setting files. We actually output USE="" in make.conf, so we also put it in here!
    for f in package_flags_environment:
        if f not in results:
            results[f] = ''
        for p in package_flags_environment[f]:
            results[f] = p
            if f == 'make.conf' and p == 'USE':
                results[f] += '= "'
            elif f == 'make.conf':
                continue
            if True in package_flags_environment[f][p]:
                for pos in package_flags_environment[f][p][True]:
                    results[f] += pos
                    results[f] += ' '
            if False in package_flags_environment[f][p]:
                for neg in package_flags_environment[f][p][False]:
                    results[f] += ' -'
                    results[f] += neg
            if f == 'make.conf' and p == 'USE':
                results[f] +='"'
    return results


# This deals with the setup, copying, and file-munging needed to transform a cpu config and a user flags config into our ./work/portage directory
# If no arguments are provided, it will simply use the default (blank, unoptimized) configuration with no packages.
def checkout_config(cpu_conf = 'zentoo/default', flags_conf : List[str] = [], debug = False):
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
    if not os.path.isdir(global_flags_path):
        print('Global (user-defined) Portage/flags config directory at ' + global_flags_path + ' does not exist.')
        return False
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not cpu_conf == '':
        if os.path.isdir(cpu_path + cpu_conf):
            custom_cpu = True
        else:
            print('The user-provided CPU config directory at ' + cpu_path + cpu_conf + ' does not exist.')
            return False
    if debug:
        print('Checking for the existence of local flagsets')
    flagsets_to_add = []
    if len(flags_conf) > 0: # Check out what's inside our list of flagset
        for flg in flags_conf:
            flg = flg.strip()
            if flg == '':
                continue
            #if flg[0] == '@':
            #    flg = flg[2:]
            if os.path.isdir(flagset_path + flg):
                custom_flags = True
                flagsets_to_add.append(flg)

            else:
                print('The user-provided local Portage/flags directory at ' + flagset_path + flg  + ' does not exist.')
                return False
    print(flags_conf)

    if debug:
        print('Setting up work env')
    # Here, we deal with the patches directory; first we do the common ones, then we do all the locals!
    sync_patches_str = ''
    if os.path.isdir(global_flags_path + 'patches'):
        sync_patches_str += ' && rsync -aHVqv ' + global_flags_path + 'patches/* ' + output_path + 'patches'
    for addme in flagsets_to_add:
        if os.path.isdir(flagset_path + addme + 'patches'):
            sync_patches_str += ' && rsync -aHXqv ' + flagset_path + addme + 'patches/* ' + output_path + 'patches'
    # We now add package sets. These are universal.
    code = os.system('rsync -aHXqv ./config/package.sets/* ' + output_path + 'sets ' + sync_patches_str) 
    if not code == 0:
        return False
    # Wow that was easy!
    for d in (flagset_path, global_flags_path, flags_include_path):
        code = os.system('cp ' + d + 'bashrc work/portage')
        if code == 0: # To ensure the operation happens in-line with the rest of the script. TODO: Make this less ugly
            continue  
    package_vars = dict() # Initialize the package flags dictionary
    portage_vars = dict() # Initialize the portage flags dictionary
    for p in (flags_include_path, global_flags_path): # Fill with info from the default config directories.
        collect_package_flags(p, '', package_vars)
        collect_portage_vars(p, '', portage_vars)
    if custom_cpu: # If our cpu flags get set, ingest them too!
        collect_portage_vars(cpu_path + cpu_conf, cpu_conf, portage_vars)
    if custom_flags: # This is where most of the collection is likely to occur. We now do some serious looping!
        for flagset in flagsets_to_add:
            #for flagset in line.split(' '):
                #flagset = flagset.strip() # Necessary to reassign?
                if len(flagset) > 0:
                    print('Collecting vars with flagset ' + flagset)
                    collect_package_flags(flagset_path + flagset, flagset, package_vars)
                    collect_portage_vars(flagset_path + flagset, flagset, portage_vars)
    #if debug:
    print(package_vars)
    print(portage_vars)

    # We now collect all the filenames and create our directory structure for the output
    all_files = []
    for f in package_vars:
        all_files += f
    for f in portage_vars:
        all_files += f

    # Make the paths needed to recreate
    create_output_directory_structure(all_files)

    # Now we can put back everything into their respective files.
    files_to_contents = recreate_output_files(portage_vars, package_vars, True)
    print(files_to_contents)
    for v in files_to_contents:
        write_file_lines(v, files_to_contents[v])

    return True


# This will ensure that user-defined sets of Portage configurations listed in a subdirectory of ./config/stage.defines/ actually all exist! 
def check_if_portage_sets_present(portage_sets : List[str]):
    for line in portage_sets:
        for token in line.split():
            token = token.strip()
            if len(token) > 0:
                if token[0] == '@':
                    token = token[1:]
            if not os.path.isdir(flagset_path + token):
                print(msg_prefix + 'Local portage directory not found: ' + flagset_path + token + ', while seeking out attached sets.')
                return False
    return True


# This turns a stage.defines config into a ./work/portage directory
# The second argument represents things that the caller needs to run afterwards.
def stage3_config(user_stage, todo : Dict[str, List[str]]):
    os.system('rm -rf ./work/portage/*')
    user_stage_path = stage_path + user_stage
    if not os.path.isdir(user_stage_path):
        print(msg_prefix + 'Could not find stage definitions directory: ' + user_stage_path)
        return False
    if os.path.isfile(user_stage_path + '/cpu'):
        cpu_conf = open(user_stage_path + '/cpu').read().strip()
        if not os.path.isdir(cpu_path + cpu_conf):
            print(msg_prefix + 'CPU config directory: ' + cpu_path + cpu_conf + ' does not exist.')
            return False
    if os.path.isfile(user_stage_path + '/flags'):
        flags_conf = read_file_lines(user_stage_path + '/flags')
        if not check_if_portage_sets_present(flags_conf):
            print('Could not find all attached flagsets')
            return False
    if os.path.isfile(user_stage_path + '/packages'):
        todo['packages'] = read_file_lines(user_stage_path + '/packages')
    if os.path.isfile(user_stage_path + '/profiles'):
        todo['profiles'] = read_file_lines(user_stage_path + '/profiles')
    if os.path.isfile(user_stage_path + '/hooks'):
        todo['hooks'] = read_file_lines(user_stage_path + '/hooks')
    code = checkout_config(cpu_conf, flags_conf, True)

    if code == False:
        print('Checkout config failed')
        return False
    return True
