#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import output_path
from include.download_tarball import download_tarball
from include.gpg_setup import gpg_setup
from include.verify_tarball import verify_tarball
from include.get_tarball_name import get_tarball_name


#gpg_setup()
#download_tarball('amd64', 'default')
#download_tarball('amd64', 'musl-hardened')
verify_tarball('./gentoomuch-data/stages/stage3-amd64-musl-hardened-20210327.tar.bz2')

