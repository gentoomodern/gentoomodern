#!/usr/bin/env python3
# This code is likely to lay unused, as we don't necessarily want to implement inheritance ourselves.
# Other languages do a better job implementing it.

import os
from .gentoomuch_common import stages_defines_path, kernel_defines_path
from .kernel_munger import kernel_munger
from .portage_munger import portage_munger


def get_stage_ancestors(stage_def: str) -> []:
    return __get_ancestors_helper(path.join(stage_defines_path, stage_def))

def get_kernel_ancestors(kernel_def: str) -> []:
    return __get_ancestors_helper(path.join(kernel_defines_path, kernel_def))

def __get_ancestors_helper(base_path: str, define_name: str) -> []:
    results = []
    candidates = []
    candidates += define_name
    while True:
        curr = candidate[0]
        candidate_dir = os.path.join(base_path, curr)
        if os.path.isdir(candidate_dir):
            parents_def = os.path.join(candidate_dir, 'parents')
            if os.path.isfile(parents_def):
                brand_new_parents = read_file_lines(parents_def)
                candidates.extend(brand_new_parents)
                results.extend(brand_new_parents)
        candidates.remove(curr)
        if len(candidates) == 0:
            break
    return results
