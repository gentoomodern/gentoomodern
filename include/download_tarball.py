#!/usr/bin/env python3

import os, urllib
from .gentoomuch_common import gentoo_upstream_url, gentoo_signing_key, stages_path, asc_ext
from .verify_tarball import verify_tarball
from .containerize import containerize


# This function/method downloads a stage, its manifest, and its signature.
# It then verifies the tarball and it successful, turns it into a docker image.
def download_tarball(arch, profile):
    tail = '-' + arch
    if profile != 'default':
        tail += '-' + profile
    url_base = gentoo_upstream_url + arch + "/autobuilds/"
    bootstrap_url = url_base + "latest-stage3" + tail + ".txt"
    print("INFO: Obtaining seed file: " + bootstrap_url)
    req = urllib.request.Request(bootstrap_url)
    lines = ''
    try:
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print("ERROR: Could not download seed file!")
        return False
    new_url = ''
    fname = ''
    fsize = -1
    figured_it_out = False
    for l in lines.split('\n'):
        if l == '' or l[0] == '#':
            continue
        words = l.split()
        nodes = words[0].split('/')
        fname = nodes[len(nodes) - 1]
        new_url = url_base + '/' + words[0]
        fsize = int(words[1])
        figured_it_out = True
    if not figured_it_out:
        print("ERROR: Could not munge stage3 path from seed.")
        return False

    for suffix in (asc_ext, ''):
        req = urllib.request.Request(new_url + suffix)
        print("INFO: Getting file " + fname + suffix + " from " + new_url + suffix)
        try:
            with urllib.request.urlopen(req) as response:
                if suffix == '':
                    with open(stages_path + fname + suffix, 'wb') as f:
                        f.write(response.read())
                        actual_size = os.stat(stages_path + fname + suffix).st_size
                    if actual_size != fsize:
                        print('ERROR: Downloaded size mismatch for ' + fname + '.  Intended: ' + fsize + '. Actual: ' + actual_size)
                        return False
                    print("INFO: Downloaded file " + stages_path + fname + suffix)
                else:
                    if os.path.isfile(os.path.join(stages_path, fname + suffix)):
                        os.remove(os.path.join(stages_path, fname + suffix))
                    with open(stages_path + fname + suffix, 'wb') as f:
                        f.write(response.read())

        except urllib.error.HTTPError as e:
            print("ERROR: " + fname + suffix + " not found at " + new_url + suffix)
            return False
    if verify_tarball(stages_path + fname + suffix):
        # Dockerize that thing, ya'll
        print("INFO: Containerizing upstream tarball")
        return containerize(fname + suffix, arch, profile, '', bool(True))
