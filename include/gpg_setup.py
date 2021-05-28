#!/usr/bin/env python3

import os, gnupg
from .gentoomuch_common import gpg_path, gentoo_signing_key

def gpg_setup():
    os.system('rm -rf ' + gpg_path + '*')
    gpg = gnupg.GPG(gnupghome = gpg_path)
    os.system('echo "honor-http-proxy\ndisable-ipv6" >> ' + gpg_path + 'dirmgnr.conf')
    import_result = gpg.recv_keys('hkps://keys.gentoo.org', gentoo_signing_key)
