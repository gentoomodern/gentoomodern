#!/usr/bin/env python3

import os, requests
from .gentoomuch_common import stages_path, gentoo_upstream_url, gentoo_signing_key


# This function/method downloads a stage, its manifest, and its signature.
def download_tarball(arch, profile):
    tail = '-' + arch
    if profile != 'default':
        tail += '-' + profile
    url_base = gentoo_upstream_url + arch + "/autobuilds/"
    bootstrap_url = url_base + "latest-stage3" + tail + ".txt"
    print("Obtaining seed file: " + bootstrap_url)
    r = requests.get(bootstrap_url)
    if r.status_code != 200:
       exit("Seed file not found!")
    lines = r.content.decode(r.encoding)
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
        exit("Could not munge stage3 path from seed.")
    
    for suffix in ('.DIGESTS', '.DIGESTS.asc', ''):
        r = requests.head(new_url + suffix)
        if r.status_code == 200:
            print("Getting file " + fname + suffix + " from " + new_url + suffix)
            r = requests.get(new_url)
            with open(stages_path + fname + suffix, 'wb') as f:
                f.write(r.content)
            if suffix == '':
                actual_size = os.stat(stages_path + fname).st_size
                if actual_size != fsize:
                    exit('Downloaded size mismatch for ' + fname + '.  Intended: ' + fsize + '. Actual: ' + actual_size)
            print("Success! We have downloaded " + stages_path + fname + suffix)
        else:
            exit("File " + fname + suffix + " not found at " + new_url + suffix)

