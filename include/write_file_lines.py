#!/usr/bin/env python3

import os


def write_file_lines(filename, lines):
    f = open(filename, 'w')
    f.writelines(lines)
    f.close()
