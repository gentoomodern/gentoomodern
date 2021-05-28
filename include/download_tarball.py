#!/usr/bin/env python3

import os, requests
from .gentoomuch_common import gentoo_upstream_url, gentoo_signing_key

# This function/method will be used to download a stage, its manifest, and its signature.
def download_tarball(output, arch, profile, upstream = False):
    tail = ("-upstream" if bool(upstream) else "-local")
    if upstream
    r = requests.get()
        
