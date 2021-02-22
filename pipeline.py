#!/usr/bin/env python3

import os

def run_container(root, command):
    return os.system("docker-compose run " + root + " " + command)

def checkout_config(branch):
    return os.system("git -C config checkout " + branch)

buildmaster = 'bootstrap'

code = run_container(buildmaster, "emerge --sync")




def rebuild(packageset):
    return "emerge -uDkq --changed-use @" + packageset

rebuild_emptytree = "emerge -uDkq --changed-use --emptytree @world"


# We run the initial bootstrap
if code == 0:
    checkout_config("bootstrap")
    code = run_container(buildmaster, rebuild_emptytree)

# We can now recompile libcap with its default options again.
if code == 0:
    checkout_config("bootstrap-2")
    code = run_container(buildmaster, rebuild_emptytree)
    if code == 0:
        code = run_container(buildmaster, rebuild("autogentoo/build-server"))
        


