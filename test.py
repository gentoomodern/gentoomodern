#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import output_path
from include.download_tarball import download_tarball


download_tarball('amd64', 'default')
download_tarball('amd64', 'musl-hardened')
