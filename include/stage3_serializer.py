#!/usr/bin/env python3

# This saves out a named tarball of a given stage define.

import os, sys, re
from include.gentoomuch_common import read_file_lines, write_file_lines
from include.portage_directory_combiner import portage_directory_combiner


