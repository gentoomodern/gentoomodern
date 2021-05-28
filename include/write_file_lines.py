#!/usr/bin/env python3

import os


def write_file_lines(filename, lines, uid = -1, gid = -1):
    f = open(filename, 'w')
    f.writelines(lines)
    f.close()
    if uid > 0:
        if gid < 0:
            os.chown(filename, uid, uid)
        else:
            os.chown(filename, uid, gid)
