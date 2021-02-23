#!/usr/bin/env python3

import os


def run_container(root, command):
    return os.system("docker-compose run " + root + " " + command)

#TODO: Split Make.conf into separate files

def checkout_config(branch):
    return os.system("git -C config checkout " + branch)

def rebuild(packageset):
    return "emerge -uDkq --changed-use @" + packageset

def install(packageset):
    return "FEATURES='usepkgonly' " + rebuild(packageset)

buildmaster = 'autogentoo-builder'
packager = "autogentoo-packager"
package_host = "autogentoo-package-host"
git_worker = "autogentoo-git-worker"

#code = run_container(buildmaster, "emerge --sync")

rebuild_emptytree = "emerge -uDkq --changed-use --emptytree @world"

# We run the initial bootstrap
#if code == 0:
checkout_config("bootstrap")
#code = run_container(buildmaster, rebuild_emptytree)

# We can now recompile libcap with its default options again.
#if code == 0:
checkout_config("bootstrap-2")
code = run_container(buildmaster, 'bash -c \'' + rebuild_emptytree + " && " + rebuild("autogentoo/build-server") +'\'')
    #if code == 0:
    #    code = run_container(buildmaster, rebuild("autogentoo/build-server"))
