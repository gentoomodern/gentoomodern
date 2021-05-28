#!/usr/bin/env python3

import re
from .gentoomuch_common import portage_output_path, global_config_path, local_config_basepath, cpu_path


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
