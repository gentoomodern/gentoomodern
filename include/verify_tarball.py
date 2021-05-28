#!/usr/bin/env python3

import gnupg
from .gentoomuch_common import gpg_path, stages_path, digests_ext, asc_ext
from .get_tarball_name import get_tarball_name

def verify_tarball(filename):
    gpg = gnupgGPG(gnupghome = gpg_path)
    verified = gpg.verify_file(open(stages_path + name + digests_ext), stages_path + name + asc_ext)
