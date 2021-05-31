#!/usr/bin/env python3

import os, gnupg, hashlib
from .gentoomuch_common import stages_path, gpg_path, asc_ext
from .read_file_lines import read_file_lines


def verify_tarball(filepath):
    gpg = gnupg.GPG(gnupghome = gpg_path)
    filename = os.path.relpath(filepath, stages_path)
    print("INFO: Verifying signature of file " +  filename)
    asc_file = open(filepath + asc_ext, 'rb').read()
    if not gpg.verify(asc_file):
        print("ERROR: Failed to verify signature file: " + filename + asc_ext)
        return False
    found = False
    lines = asc_file.decode('ascii').split('\n')
    ctr = 0
    # We are going to find the line in the .asc file that corresponds to our SHA512 sig and obtain it.
    while not found:
        if ctr + 1 == len(lines):
            exit("ERROR: Reached end of " + filename + asc_ext + " without finding the tarball's SHA512 hash.")
            # return False
        if lines[ctr]  == '# SHA512 HASH':
            desired_sha512 = lines[ctr + 1].split(' ')[0]
            found = True
        ctr += 1
    print("INFO: Seeking hash:   " + desired_sha512)
    sha512 = hashlib.sha512()
    BLOCK_SIZE = 65536
    with open(filepath, 'rb') as f:
        buf = f.read(BLOCK_SIZE)
        while len(buf) > 0:
            sha512.update(buf)
            buf = f.read(BLOCK_SIZE)
    print("INFO: Hashed value is " + sha512.hexdigest())
    if desired_sha512 != sha512.hexdigest():
        exit("ERROR: Wrong SHA512 for " + filename)
    return True
