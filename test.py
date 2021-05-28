#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import output_path
from include.download_tarball import download_tarball
from include.gpg_setup import gpg_setup
from include.verify_tarball import verify_tarball
from include.get_tarball_name import get_tarball_name


# download_tarball('amd64', 'default')
# download_tarball('amd64', 'musl-hardened')
gpg_setup()
# verify_tarball(

