#!/usr/bin/env python3

def read_file_lines(filename):
    f = open(filename)
    lines = f.readlines()
    return lines

def write_file_lines(filename, lines):
    f = open(filename, 'w')
    f.writelines(lines)
    f.close()
