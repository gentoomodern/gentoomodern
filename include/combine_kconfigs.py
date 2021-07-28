#!/usr/bin/env python3

import os
from .kernel_munger import kernel_munger
from .gentoomodern_common import kconf_frags_path 

def combine_kconfigs(configs : [str]) -> bool:
    results = kernel_munger()
    for c in configs:
        p = os.path.join(kconf_frags_path, c)
        if os.path.isfile:
            if not results.munge(p):
                print("A conflict was found when adding kernel config " + c + " to the output config. Not continuing this kernel's assembly.")
                return False
        else:
            print("Kernel config " + c + " has not been found.")
            return False
