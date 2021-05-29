#!/usr/bin/env python3

import os, gnupg, hashlib
from .gentoomuch_common import gpg_path, digests_ext, asc_ext
from .read_file_lines import read_file_lines
from .get_tarball_name import get_tarball_name

def verify_tarball(filepath):
    gpg = gnupg.GPG(gnupghome = gpg_path)
    print(filepath + asc_ext)
    print(filepath + digests_ext)
    asc_file = open(filepath + asc_ext, 'rb').read()
    if not gpg.verify(asc_file):
        print("ERROR: Failed to verify " + filepath + asc_ext + " signature file")
        return False
    found = False
    lines = asc_file.decode('ascii').split('\n')
    ctr = 0
    # We are going to find the line in the .asc file that corresponds to our SHA512 sig and obtain it.
    while not found:
        if ctr + 1 == len(lines):
            print("ERROR: Reached end of DIGESTS.asc without finding SHA215 hash. This is worth noticing.")
            return False
        if lines[ctr]  == '# SHA512 HASH':
            desired_sha512 = lines[ctr + 1].split(' ')[0]
            print('Seeking SHA512: ' + desired_sha512)
            found = True
        ctr += 1
    print("Attempting to hash. Needing: " + desired_sha512)
    sha512 = hashlib.sha512()
    BLOCK_SIZE = 65536
    with open(filepath, 'rb') as f:
        buf = f.read(BLOCK_SIZE)
        while len(buf) > 0:
            sha512.update(buf)
            buf = f.read(BLOCK_SIZE)
    print("Hashed file value is " + sha512.hexdigest())
    print(sha512.hexdigest() == desired_sha512)
    return bool(desired_sha512 == sha512.hexdigest())
