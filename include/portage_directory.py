#!/usr/bin/env python3

import sys, os 
from .gentoomuch_common import read_file_lines, write_file_lines, read_by_tokens, output_path, config_dir, stage_defines_path, cpu_path, pkgset_path, local_config_basepath, hooks_path, kernel_path, global_config_path, get_cleaned_path, debug
from .munger import munger

class portage_directory:
    def __init__(self):
        self.accumulators = dict() #[str, munger]

    def ingest(self, local_path):
        if debug:
            print ("[portage_directory] Ingesting " + local_path)
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
                    print('[munger] Processing ' + current_file)
                if not current_file in self.accumulators:
                    self.accumulators[current_file] = munger(current_path, f)
                for line in read_file_lines(os.path.join(dirpath, f)): # Here we do our actual file-reading
                    self.accumulators[current_file].ingest(line)
                        # sys.exit('portage_directory.setup() - ERROR - Could not ingest ' + current_file + ' due to line : ' + line)
                if debug:
                    print('[munger] Done ingesting ' + current_file)

    def writeout(self):
        for m in self.accumulators.values():
            current_output_dir = os.path.join(output_path, m.get_current_directory())
            print(current_output_dir)
            if not os.path.isdir(current_output_dir):
                os.mkdir(current_output_dir)
            current_output_file = os.path.join(current_output_dir, m.get_current_filename())
            if not os.path.isfile(current_output_file):
                text = m.get_text()
                if len(text) > 0:
                    write_file_lines(current_output_file, text)
                else:
                    if debug:
                        print("[munger] Empty file " + current_output_file + " when writing out")

