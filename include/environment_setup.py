# In this, we create all the folders necessary to recreate our desired portage filestructure.
def create_output_directory_structure(filepaths : List[str]):
    for fpath in filepaths: 
        #if debug:
        print('File ' + fpath)
        expanded_fpath = fpath.split('/')
        #if debug:
        print(expanded_fpath)
        print('Expanded fpath (list) length = ' + str(len(expanded_fpath)))
        prefix = output_path
        if len(expanded_fpath) > 1: # If we're still considering a directory and not a file
            #if debug:
            print('Going deeper into the filestructure') # TODO: Make more sense
            for p in expanded_fpath: # The last element is the filename itself
                prefix += '/'
                prefix += p
                print('prefix = ' + prefix)
                if not os.path.isdir(prefix):
                    #if debug:
                    print('Making directory ' + prefix)
                    os.mkdir(prefix) # Now we finally make our directory. Is there a better way to do this???


# This returns a dictionary containing the file paths. Each has its contents stored in a list of strings, one for each line.
def recreate_output_files(portage_conf_environment : Dict[str, List[str]], package_flags_environment : Dict[str, Dict[str, Dict[bool, List[str]]]]):
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
            if flg[0] == '@':
                flg = flg[1:]
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
    # Wow that was easy! Now we can iterate over each
    for d in (flagset_path, global_flags_path, flags_include_path):
        code = os.system('cp ' + d + 'bashrc work/portage')
        if code == 0: # To ensure the operation happens in-line with the rest of the script. TODO: Make this less ugly
            continue  
    package_vars = dict() # Initialize the package flags dictionary
    for p in (flags_include_path, global_flags_path): # Fill with info from the default config directories.
        collect_portage_flags(p, '', package_vars)
    if custom_flags: # This is where most of the collection is likely to occur. We now do some serious looping!
        for flagset in flagsets_to_add:
                if len(flagset) > 0:
                    print('Collecting vars with flagset ' + flagset)
                    collect_portage_flags(flagset_path + flagset, flagset, package_vars)
    # if debug:
    print(package_vars)

    # We now collect all the filenames and create our directory structure for the output
    all_files = []
    for f in package_vars:
        all_files += f

    # Now we can put back everything into their respective files.
    files_to_contents = recreate_output_files(portage_vars, package_vars, True)
    print(files_to_contents)
    for v in files_to_contents:
        write_file_lines(output_path + v, files_to_contents[v])

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
