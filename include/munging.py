#!/usr/bin/env python3

import sys, os, re
from typing import Dict, List, Set
from .gentoomuch_common import read_file_lines, write_file_lines, read_by_tokens, output_path, config_dir, stage_defines_path, cpu_path, pkgset_path, local_config_basepath, hooks_path, kernel_path, global_config_path, get_cleaned_path

debug = True

dont_munge_files = (['', 'bashrc'], ['', 'modules'], ['', 'README.md'], ['', 'mirrors'], ['', 'color.map'])
dont_munge_dirs = ('sets', 'patches', 'savedconfig')


class stage3:
    def __init__(self):
        self.accumulators = dict() #[str, munger]

    def ingest(self, local_path):
        if debug:
            print ("[stage3] Ingesting " + local_path)
        for (dirpath, dirnames, filenames) in os.walk(local_path):
            current_path = get_cleaned_path(dirpath, local_path)
            for d in dirnames:
                outdir = os.path.join(output_path, d)
                if not os.path.isdir(outdir):
                   os.mkdir(outdir)
                    #if debug:
                    #    print('Creating directory ' + d + ' in work/portage')
            for f in filenames:
                current_path = get_cleaned_path(dirpath, local_path)
                print('[munger] current (cleaned) path = ' + current_path)
                current_file = os.path.join(current_path, f)
                if debug:
                    print('[stage3] Processing ' + current_file)
                if not current_file in self.accumulators:
                    self.accumulators[current_file] = munger(current_path, f)
                for line in read_file_lines(os.path.join(dirpath, f)): # Here we do our actual file-reading
                    self.accumulators[current_file].ingest(line.strip())
                        # sys.exit('stage3.setup() - ERROR - Could not ingest ' + current_file + ' due to line : ' + line)
                if debug:
                    print('[stage3] Done ingesting ' + current_file)

    def writeout(self):
        for m in self.accumulators.values():
            current_output_dir = os.path.join(output_path, m.get_current_directory())
            print(current_output_dir)
            if not os.path.isdir(current_output_dir):
                os.mkdir(current_output_dir)
            current_output_file = os.path.join(current_output_dir, m.get_current_filename())
            if not os.path.isfile(current_output_file):
                text = m.get_text()
                if len(text) == 0:
                    write_file_lines(current_output_file, m.get_text())
                else:
                    if debug:
                        print("Empty file " + current_output_file + " when writing out")

class munger:
    # This identifies and deduplicates flags
    # It will verify for set/unset combinations and return False upon spotting one.
    # This allows the user to avoid potential surprises.
    def ingest(self, line):
        atom = self.__get_atom_name(line)
        if atom == "":
            if debug:
                print("munger.ingest() - DEBUG - Empty atom name. Skipping...") 
        else:
            flags_str = re.sub('^' + re.escape(atom), '', line)
            # Now, we figure out whether or not the line gets passthrough or has its values held into dictionary.
            if self.current_file == "make.conf" and self.current_directory == "":
                if self.__is_atom_portage_var(atom):
                    self.__ingest_use_flags(atom, flags_str)
            elif self.__is_file_pkg_flags_syntax():
                self.__ingest_use_flags(atom, flags_str)
            elif self.__is_file_simple_atom_syntax():
                self.__ingest_atom(atom)
            else:
                self.unmodified_lines.append(line)

    def get_text(self):
        results = self.unmodified_lines
        if self.current_directory == '' and self.current_file == 'make.conf':
            results.append(self.__get_text_make_conf_syntax())
        return results

    def get_current_directory(self):
        return self.current_directory

    def get_current_filename(self):
        return self.current_file

    def __init__(self, current_dir, current_file):
        print('[munger] create with dir = ' + current_dir + ', and current file = ' + current_file)
        self.use_flags = dict() #[str, Dict[bool, List[str]]] 
        self.unmodified_lines = list() #[str]
        self.atoms = set()
        self.current_directory = current_dir
        self.current_file = current_file

    def __is_atom_portage_var(self, atom):
        return bool(re.search('^USE[=]', atom)) or bool(re.search('^CPU_FLAGS_', atom)) or bool(re.search('^ACCEPT_', atom))

    def __is_file_simple_atom_syntax(self):
        files = ('package.mask', 'package.unmask')
        if self.current_directory == '' and self.current_file in files:
            return True
        else:
            return False

    def __is_file_pkg_flags_syntax(self):
        files = ('package.accept_keywords', 'package.use', 'package.env')
        if self.current_directory == 'package.use' or (self.current_directory == '' and self.current_file in files):
            return True
        else:
            return False
    
    def __get_text_make_conf_syntax(self):
        results = self.unmodified_lines
        for atom in self.use_flags.keys():
            counter = 0
            line = atom + '='
            for flag in self.use_flags[atom][True]:
                if counter > 0:
                    line += ' '
                line += flag
                counter += 1
            for flag in self.use_flags[atom][False]:
                if counter > 0:
                    line += ' -'
                else:
                    line += '-'
                line += flag
                line += '"'
            results.append(line)
        return results

    def __get_text_simple_atom_syntax(self):
        results = []
        for atom in self.atoms:
            if not atom[0] == '#':
                results.append(atom)
        return results
    
    def __get_atom_name(self, line):
        if not re.match('(\S)+', line): # Only proceed if we don't have an empty line... Those make the regex engine crash
            return ""
        if debug:
            print('Inside munger - Line: ' + line)
        atom_name = re.match('^\S+', self.__strip_quotes(line)).group() # Get the first block of non-whitespace characters
        if atom_name[0] == '#': # Skip comments
            return ""
        else:
            return atom_name

    def __strip_quotes(self, line):
        return re.sub('(\'|")+', ' ', line) # Strip out them quotes!

    def __get_canonical_flagname(self, line): # Get rid of the negative signs in front.
        return re.sub('^(-)+', '', line)

    def __get_canonical_flagname_test(self):
        if not self.__get_canonical_flagname('silly-thing/dontchangeme') == 'silly-thing/dontchangeme':
            sys.exit("munger.get_canonical_flagname() - UNIT TEST FAIL - Should not change flags' contents.")
        if not self.__get_canonical_flagname('-silly-thing/testme') == 'silly-thing/testme':
            sys.exit('munger.get_canonical_flagname() - UNIT TEST FAIL - Single neg.')
        if not self.__get_canonical_flagname('--silly-thing/testmemore') == 'silly-thing/testmemore':
            sys.exit('munger.get_canonical_flagname() - UNIT TEST FAIL - Multiple negative signs.')
        if not self.__get_canonical_flagname('-') == '':
            sys.exit('munger.get_canonical_flagname() - UNIT TEST FAIL - Empty flag.')

    def __ingest_atom(self, atom):
        if not atom[0] == '#':
            self.atoms.add(atom)
    
    def __ingest_use_flags(self, atom_name, flags_str):
        for candidate_flag in flags_str.split():
            candidate_flag = candidate_flag.strip()
            if debug:
                print('munger.ingest_use_flags() - DEBUG - Examining flag "' + candidate_flag + '"')
            if candidate_flag[0] == '#': # Skip comments
                break
            if candidate_flag == "" or candidate_flag == '=':
                continue
            if atom_name not in self.use_flags:
                self.use_flags[atom_name] = dict()
                self.use_flags[atom_name][True] = []
                self.use_flags[atom_name][False] = []
            flag_abs = self.__get_canonical_flagname(candidate_flag)
            is_setting = bool(flag_abs == candidate_flag)
            # Now, we actually add (or not) to our dictionary.
            if flag_abs in self.use_flags[atom_name][is_setting]: # If it's already in our list, we can move on. That's how we implement deduplication!
                continue
            elif flag_abs in self.use_flags[atom_name][not is_setting]: # If that flag is in converse list, then adding the opposite flag will only cause confusion.
                return False
            else: # We now can append anything that has passed the previous tests.
                self.use_flags[atom_name][is_setting].append(flag_abs)
        return True

    def __ingest_use_flags_test(self):
        desired = { 'AB': { True: ['nice-enough'], False: ['awful'] } }
        old_use_flags = self.use_flags
        self.use_flags.clear()
        test_1 = "AB='-awful nice-enough -awful"
        if not self.__ingest_use_flags(test_1):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 1. Should return true.')
        if not self.use_flags  == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 1. Bad results.')
        self.use_flags.clear()
        test_2 = 'AB = -awful nice-enough -awful'
        if not self.__ingest_use_flags(test_2):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 2. Should return true.')
        if not self.use_flags == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 2. Bad results.')
        self.use_flags.clear()
        test_3 = 'AB="-awful nice-enough awful"'
        if not self.__ingest_use_flags(test_3):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 3 (yes and no). Should return false.')
        if not self.use_flags == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 3 (yes and no). Bad results.')
        self.__use_flag.clear()
        test_4 = ["AB='nice-enough -awful nice-enough nice-enough'"]
        if not self.__ingest_use_flags(test_4):
            sys.exit('munger.ingest() - UNIT TEST FAIL - 4. Should return true.')
        if not self.use_flags == desired:
            sys.exit('munger.ingest() - UNIT TEST FAIL - 4. Bad results.')
        self.use_flags.clear()
        self.use_flags = old_use_flags
