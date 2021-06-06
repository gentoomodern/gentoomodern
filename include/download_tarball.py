#!/usr/bin/env python3

import os, urllib
from .gentoomuch_common import gentoo_upstream_url, gentoo_signing_key, stages_path, asc_ext
from .verify_tarball import verify_tarball
from .containerize import containerize

#################################################################################
# This function/method downloads a stage, its manifest, and its signature.      #
# It then verifies the tarball and it successful, turns it into a docker image. #
#################################################################################
# TODO: Check whether file exists locally.
def download_tarball(arch, profile):
    tail = '-' + arch
    if profile != 'default':
        tail += '-' + profile
    url_base = gentoo_upstream_url + arch + "/autobuilds/"
    #####################################################################################
    # In the "root" directory of the upstream URL, for each stage we have a small file. #
    # latest-stage3-<profile>.txt                                                       #
    #####################################################################################
    if arch == 'amd64' and profile == 'x32':
        tail = '-x32'
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
    ##############################################
    # Munge the indexing file and retrieve info. #
    ##############################################
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
    tarball_path            = os.path.join(stages_path, fname)
    tarball_asc             = tarball_path + asc_ext
    sig_url                 = new_url + asc_ext
    print("TARBALL PATH " + tarball_path)
    ##################
    # ASC extension. #
    ##################
    req = urllib.request.Request(sig_url)
    if os.path.isfile(tarball_asc):
        os.remove(tarball_asc)
    try:
        with urllib.request.urlopen(req) as response:
            with open(tarball_asc, 'wb') as f:
                f.write(response.read())
    except urllib.error.HTTPError as e:
        print("ERROR: " + fname + asc_ext + " not found at " + sig_url)
        return False
    ############
    # Tarball. #
    ############
    print("INFO: Getting file " + fname + " from " + new_url)
    req = urllib.request.Request(new_url)
    try:
        with urllib.request.urlopen(req) as response:
            with open(tarball_path, 'wb') as f:
                f.write(response.read())
                actual_size = os.stat(tarball_path).st_size
                if actual_size != fsize:
                    print('ERROR: Downloaded size mismatch for ' + fname + '.  Intended: ' + fsize + '. Actual: ' + actual_size)
                    return False
                print("INFO: Downloaded file " + tarball_path)
    except urllib.error.HTTPError as e:
        print("ERROR: " + fname + asc_ext + " not found at " + sig_url)
        return False
    

    if verify_tarball(tarball_path):
        # Dockerize that thing, ya'll
        print("INFO: Containerizing upstream tarball")
        return containerize(fname, arch, profile, '', bool(True))
