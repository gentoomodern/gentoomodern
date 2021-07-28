#!/usr/bin/env python3

import os, urllib
from .gentoomodern_common import gentoo_upstream_url, gentoo_signing_key, stages_path, asc_ext
from .verify_tarball import verify_tarball
from .containerize import containerize



class downloader:
    def __init__(self: str, arch: str, profile: str, output_path: str, url: str):
        self.arch = arch
        self.profile = profile
        self.output_path = output_path
        self.url = url

    
    def get(self) -> bool:
        
        return True

    # The first file that gets downloaded; it has the name and filesize of the tarball.
    def __seed(self) -> bool:
        tail = '-' + self.arch
        if profile != 'default':
            tail += '-' + self.profile
        url_base = gentoo_upstream_url + self.arch + "/autobuilds/"
        # This one is named all wierd. :P
        if self.arch == 'amd64' and self.profile == 'x32':
            tail = '-x32'
        bootstrap_url = self.url + "latest-stage3" + tail + ".txt"
        print("INFO: Obtaining seed file: " + self.url)
        req = urllib.request.Request(bootstrap_url)
        lines = ''
        try:
            with urllib.request.urlopen(req) as response:
                lines = response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print("ERROR: Could not download seed file!")
            return False
        return True


    def __asc(self):
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
        tarball_path = os.path.join(stages_path, fname)
        return True


    def __tarball(self) -> bool:
        print("TARBALL PATH " + tarball_path)
        for suffix in (asc_ext, ''):
            req = urllib.request.Request(new_url + suffix)
            print("INFO: Getting file " + fname + suffix + " from " + new_url + suffix)
            try:
                with urllib.request.urlopen(req) as response:
                    if suffix == '':
                        with open(tarball_path + suffix, 'wb') as f:
                            f.write(response.read())
                            actual_size = os.stat(tarball_path + suffix).st_size
                        if actual_size != fsize:
                            print('ERROR: Downloaded size mismatch for ' + fname + '.  Intended: ' + fsize + '. Actual: ' + actual_size)
                            return False
                        print("INFO: Downloaded file " + tarball_path + suffix)
                    else:
                        if os.path.isfile(tarball_path + suffix):
                            os.remove(tarball_path + suffix)
                        with open(tarball_path + suffix, 'wb') as f:
                            f.write(response.read())
            except urllib.error.HTTPError as e:
                print("ERROR: " + fname + suffix + " not found at " + new_url + suffix)
                return False
        return True


# This function/method downloads a stage, its manifest, and its signature.
# It then verifies the tarball and it successful, turns it into a docker image.
# TODO: Implement verification of present file
#def download_tarball(arch: str, profile: str):
#    if verify_tarball(tarball_path + suffix):
#        # Dockerize that thing, ya'll
#        print("INFO: Containerizing upstream tarball")
#        return containerize(fname + suffix, arch, profile, '', bool(True))
