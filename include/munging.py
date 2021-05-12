#!/usr/bin/env python3

import sys, os, re
from typing import Dict, List, Set
from GentooMuchCommon import read_file_lines, write_file_lines, read_by_tokens

stage_parts = ('cpu', 'packages', 'flags', 'profile')
dont_munge_files = (['', 'bashrc'], ['', 'modules'], ['', 'README.md'], ['', 'mirrors'], ['', 'color.map')
dont_munge_dirs = ('sets', 'patches', 'savedconfig')

output_path        = './work/portage/'
config_dir         = './config/'
stage_path         = config_dir + 'stage.defines/'
cpu_path           = config_dir + 'cpu.defines/'
pkgset_path        = config_dir + 'package.sets/'
flagset_path       = config_dir + 'portage.locals/'
hooks_path         = config_dir + 'build.hooks/'
kernel_path        = config_dir + 'kernel.defines/'
global_flags_path  = config_dir + 'portage.global/'
flags_include_path = './include/portage.defaults/'

def create_output_directory(output_path, cleaned_dirpath):
    cleaned_dirpath = get_cleaned_dirpath(dirpath, config_path_in, config_name_in)
    os.mkdir(output_path + cleaned_dirpath)
    if cleaned_dirpath in dont_munge_dirs:
        if debug:
            print("create_output_directory() - DEBUG - Skipping " + cleaned_dirpath)
            return
        if not os.path.exists(output_path + cleaned_dirpath):
        if debug:
            print('create_output_directory() - DEBUG - Ingesting ' + f)
        cleaned_filepath = cleaned_dirpath + '/' + f
        if cleaned_filepath[0] == '/':
            cleaned_filepath = cleaned_filepath[1:]
        if cleaned_filepath == '': # Blank names mess things up.
            continue
        if debug:
            print('create_output_directory() - DEBUG - Filepath: ' + f + ', Filepath (cleaned): ' + cleaned_filepath)

def get_cleaned_dirpath(dirpath, config_path, config_name):
    results = re.sub(re.escape(flags_include_path)       , '', dirpath)
    results = re.sub(re.escape(global_flags_path)        , '', results)
    results = re.sub(re.escape(flagset_path)             , '', results)
    results = re.sub(re.escape(cpu_path)                 , '', results)
    results = re.sub(re.escape(config_path)              , '', results)
    results = re.sub(re.escape(config_name)              , '', results)
    results = re.sub('^/'                                , '', results)
    return results

def stage3_config(portage_config_path_in, config_name_in):
    for (dirpath, dirnames, filenames) in os.walk(portage_config_path_in):
        lines = read_file_lines(dirpath + '/' + f) # Here we do our actual file-reading
        if not ingest_file(lines):
            print("stage3_config() - ERROR - Could not ingest " + cleaned_filepath)
            return False
        if debug:
            print('Done ingesting ' + cleaned_filepath)
    return True

class munger:
    # This identifies and deduplicates flags
    # It will verify for set/unset combinations and return False upon spotting one.
    # This allows the user to avoid potential surprises.
    def ingest(self, line):
        atom = self.get_atom_name(line)
        if atom == "":
            if debug:
                print("munger.ingest() - DEBUG - Empty atom name. Skipping...") 
            continue
        flags_str = re.sub('^' + re.escape(atom), '', line)
        # Now, we figure out whether or not the line gets passthrough or has its values held into dictionary.
        if self.current_file == "make.conf" and self.current_directory == "":
            if self.is_atom_portage_var(atom) 
                self.ingest_use_flags(atom, flags_str)
        elif self.is_file_pkg_flag_syntax():
            self.ingest_use_flags(atom, flags_str)
        elif self.is_file_simple_atom_syntax():
             self.ingest_atom(atom)
        else:
            self.unmodified_lines.append(line)

    def __is_atom_portage_var(self, atom):
        return bool(re.search('^USE[=]', atom)) or bool(re.search('^CPU_FLAGS_', atom)) or bool(re.search('^ACCEPT_', atom))

    def __is_file_simple_atom_syntax(self):
        files = ('package.mask', 'package.unmask')
        if self.current_directory == '' and self.current_file in files:
            return True
        else:
            return False

    def __is_file_pkg_flags_syntax(self):
        files = ('package.accept_keywords', 'package.use', )
        if self.current_directory == 'package.use' or (self.current_directory == '' and self.current_file in files):
            return True
        else:
            return False

    def set_path(self, pathname):
        self.current_directory = pathname

    def __set_path_test(self, pathname):
        old_path = self.current_directory
        self.set_path(pathname)
        if not self.current_directory == pathname:
            system.exit("munger.set_path() - UNIT TEST FAIL")
        self.current_directory = old_path

    def set_file(self, filename):
        self.current_file = filename

    def __set_file_test(self, filename):
        old_file = self.filename
        self.set_file(filename)
        if not self.filename == filename):
            system.exit("munger.set_file() - UNIT TEST FAIL")
        self.filename = old_file

    def get_text(self):
        results = self.unmodified_lines
        if self.current_dir = '' and self.current_file == 'make.conf':
            results.append(self.get_text_make_conf_syntax())
        
    def __init__(self):
        self.use_flags = dict() #[str, Dict[bool, List[str]]] 
        self.unmodified_lines = list() #[str]
        self.atoms = set()
        self.current_file = ""
        self.current_directory = ""

    # Stub
    def __get_text_make_conf_syntax(self):
        results = unmodified_lines
        for atom in self.use_flags.keys():
            counter = 0
            line = atom
                line += '="'
            for flag in self.use_flags[atom][True]:
                if counter > 0:
                    line += ' '
                line += flag
                counter++
            for flag in self.use_flags[atom][False]:
                if counter > 0:
                    line += ' -'
                else:
                    line += '-'
                line += flag
                line += '"'
            results.append(line)
        return results

    # Stub
    def __get_text_simple_atom_syntax(self):
        results = []
        for atom in self.atoms:
            if not atom[0] == '#':
                results.append(atom)
        return results
    
    def __get_atom_name(self, line):
        if not re.match('(\S)+', line): # Only proceed if we don't have an empty line... Those make the regex engine crash
            continue
        if self.debug:
            print('Inside munger - Line: ' + line)
        atom_name = re.match('^\S+', self.strip_quotes(line)).group() # Get the first block of non-whitespace characters
        if atom_name[0] == '#': # Skip comments
            return ""
        else:
            return atom_name

    def __strip_quotes(self, line):
        return re.sub('(\'|")+', ' ', line) # Strip out them quotes!

    def __get_canonical_flagname(self, line): # Get rid of the negative signs in front.
        return re.sub('^(-)+', '', line)

    def __get_canonical_flagname_test(self):
        if not self.get_canonical_flagname('silly-thing/dontchangeme') == 'silly-thing/dontchangeme':
            sys.exit("munger.get_canonical_flagname() - UNIT TEST FAIL - Should not change flags' contents.")
        if not self.get_canonical_flagname('-silly-thing/testme') == 'silly-thing/testme':
            sys.exit('munger.get_canonical_flagname() - UNIT TEST FAIL - Single neg.')
        if not self.get_canonical_flagname('--silly-thing/testmemore') == 'silly-thing/testmemore':
            sys.exit('munger.get_canonical_flagname() - UNIT TEST FAIL - Multiple negative signs.')
        if not self.get_canonical_flagname('-') == '':
            sys.exit('munger.get_canonical_flagname() - UNIT TEST FAIL - Empty flag.')

    def __ingest_atom(self, atom):
        atoms.add(atom)
    
    def __ingest_use_flags(self, atom_name, flags_str):
        for candidate_flag in flags_str.split():
            candidate_flag = candidate_flag.strip()
            if debug:
                print('munger.ingest_use_flags() - DEBUG - Examining flag "' + candidate_flag + '"')
            if candidate_flag  == '': # Ensure we actually have text to work with
                continue
            if candidate_flag[0] == '#': # Skip comments
                break
            if candidate_flag == "" or candidate_flag == '=':
                continue
            is_setting = bool(atom_name in self.use_flags)
            flag_abs = self.get_canonical_flagname(candidate_flags)
            # Now, we actually add (or not) to our dictionary.
            if flag_abs in self.use_flags[atom_name][is_setting]: # If it's already in our list, we can move on. That's how we implement deduplication!
                continue
            elif flag_abs in self.use_flags[atom_name][not is_setting]: # If that flag is in the list for negatives, then adding a positive flag will only cause confusion.
                return False
            else:
                self.use_flags[atom_name][is_setting].append(flag_abs) # We now can append anything that has passed the previous tests.
        return True

    def __ingest_use_flags_test(self):
        desired = { 'AB': { True: ['nice-enough'], False: ['awful'] } }
        old_use_flags = self.use_flags
        self.use_flags.clear()
        test_1 = "AB='-awful nice-enough -awful"
        if not self.ingest_use_flags(test_1):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 1. Should return true.')
        if not self.use_flags  == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 1. Bad results.')
        self.use_flags.clear()
        test_2 = 'AB = -awful nice-enough -awful'
        if not self.ingest_use_flags(test_2):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 2. Should return true.')
        if not self.use_flags == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 2. Bad results.')
        self.use_flags.clear()
        test_3 = 'AB="-awful nice-enough awful"'
        if not self.ingest_use_flags(test_3):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 3 (yes and no). Should return false.')
        if not self.use_flags == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 3 (yes and no). Bad results.')
        self.use_flag.clear()
        test_4 = ["AB='nice-enough -awful nice-enough nice-enough'"]
        if not self.ingest_use_flags(test_4):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 4. Should return true.')
        if not self.use_flags == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 4. Bad results.')
        self.use_flags.clear()
        self.use_flags = old_use_flags
