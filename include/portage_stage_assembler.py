#!/usr/bin/env python3

import sys, os 
from .gentoomodern_common import portage_output_path, config_path, stage_defines_path, cpu_frags_path, pkgset_path, buildhook_frags_path, global_portage_config_path, debug, sets_output_path
from .read_file_lines import read_file_lines
from .write_file_lines import write_file_lines
from .portage_directory import portage_directory
from .patch_profile import patch_profile


class portage_stage_assembler:
    # TODO: The other things we need to do after assembly.
    # accum: Our Portagedir accumulator.
    def __init__(self):
        self.todo = dict() # Dict[str, List[str]]
        self.accum = portage_directory()
        self.msg_prefix = 'portage_stage_assembler::'
    #####################################################
    # Processes the stage definitions of a given name.  #
    # It even does the output!                          #
    #####################################################
    def process_stage_defines(self, profile, current_stage):
        msg_prefix = self.msg_prefix + 'process_stage_defines() - '
        current_stage = current_stage.strip()
        # First, we ensure our target output directory is sane.
        self.__prep()
        # Determine whether the stage defines path exists.
        current_stage_defines_path = os.path.join(stage_defines_path, current_stage)
        if not os.path.isdir(current_stage_defines_path):
            sys.exit(msg_prefix + 'Could not find stage definitions directory: ' + current_stage_defines_path)
        # Get CPU part of stage defines.
        cpu_defines_path = os.path.join(current_stage_defines_path, 'cpu')
        if not os.path.isfile(cpu_defines_path):
            sys.exit(msg_prefix + 'Could not find cpu defines file: ' + os.path.join(current_stage_defines_path, 'cpu'))
        cpu_conf = open(os.path.join(current_stage_defines_path, 'cpu')).read().strip()
        # Now we verify CPU-related info.
        local_cpu_path = os.path.join(cpu_path, cpu_conf)
        if not os.path.isdir(local_cpu_path):
            sys.exit(msg_prefix + 'CPU config directory: ' + local_cpu_path + ' does not exist.')
        # Now ingest.
        self.accum.ingest(local_cpu_path)
        # Now, we can pull in the globally-needed parts.
        self.__checkout_common_config(profile)
        # We need to get to the file in which local portage directories are written. 
        flags_defines_path = os.path.join(current_stage_defines_path, 'flags')
        if os.path.isfile(flags_defines_path):
            flags_conf = read_file_lines(flags_defines_path)
        else:
            sys.exit(msg_prefix + 'Stage3 definition flag file: ' + flags_defines_path + ' does not exist.')
        # Now we can loop over all local portages, accumulating them.
        for local in flags_conf:
            combined_path = os.path.join(local_config_basepath, local.strip())
            # Verify directory exists.
            if not os.path.isdir(combined_path):
                sys.exit(msg_prefix + 'Local portage flags config directory ' + combined_path + ' does not exist.')
            # Now ingest.
            print(msg_prefix + "Ingesting " + combined_path)
            self.accum.ingest(combined_path)
        # We add info we must use post-munge.
        combined_path = os.path.join(current_stage_defines_path, 'packages')
        if os.path.isfile(combined_path):
            self.todo['packages'] = read_file_lines(combined_path)
        combined_path = os.path.join(current_stage_defines_path, 'hooks')
        if os.path.isfile(combined_path):
            self.todo['hooks'] = read_file_lines(combined_path)
        # Now we write-out the files themselves
        self.accum.writeout()

    def todo(self):
      return self.todo

    def __prep(self):
        msg_prefix = self.msg_prefix + '__prep() - '
        if debug:
            print(msg_prefix + 'Prepping munged portagedir environment.')
        if not os.path.isdir(portage_output_path):
            os.mkdir(portage_output_path)
        code = os.system('rm -rf ' + os.path.join(portage_output_path, '*'))
        if not code == 0:
            sys.exit(msg_prefix + 'Could not clean output dir')

    def __checkout_common_config(self, profile):
        msg_prefix = self.msg_prefix + '__checkout_common_config() - '
        # Verify existence of global config directory.
        if not os.path.isdir(global_portage_config_path):
            sys.exit(msg_prefix + 'Global Portage config directory at ' + global_portage_config_path + ' does not exist.')
        # Ingest that thing.
        self.accum.ingest(global_portage_config_path)
        # Here, we deal with the (package) sets and patches.
        rsync_cmd = 'rsync -aHXvq '
        patch_profile(profile)
        if not os.path.isdir(sets_output_path):
            os.mkdir(sets_output_path)
        sync_sets_str = rsync_cmd + os.path.join(pkgset_path, '*') + ' ' + sets_output_path
        def print_rsync_error(tag):
            sys.exit(msg_prefix + "Could not rsync " + tag + " with error code: " + str(code))
        # We now add package sets. These are universal.
        code = os.system(sync_sets_str)
        if not code == 0:
            print_rsync_error('sets')
