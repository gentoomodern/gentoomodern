#!/usr/bin/env python3

import os


buildmaster = 'autogentoo-builder'
#packager = "autogentoo-packager"
package_host = "autogentoo-package-host"
git_worker = "autogentoo-git-worker"

rebuild_emptytree = "emerge -uDkq --changed-use --emptytree @world"

def prep_config():
    return os.system('rsync -aXHp config build')

def run_container(root, command):
    return os.system("docker-compose run " + root + " " + command)

def create_mutable_container(root, name):
    # TODO:
    # Make temp Dockerfile
    # Build our Dockerfile
    # Assign the name
    return os.system()

#TODO: Git checkout in an immutable manner
def checkout_config(branch):
    return os.system("git -C build/config checkout " + branch)

def build(packageset):
    return "emerge -uDkq --changed-use @" + packageset

def install(packageset):
    return "FEATURES='usepkgonly' " + build(packageset)


#TODO: Optimize into a single docker-compose run
# We run the initial bootstrap
#if code == 0:
prep_config()
checkout_config("bootstrap")
code = run_container(buildmaster, rebuild_emptytree)

# We can now recompile libcap with its default options again.
if code == 0:
    checkout_config("bootstrap-2")
    code = run_container(buildmaster, 'bash -c \'' + rebuild_emptytree + " && " + build("autogentoo/build-server") +'\'')
    #if code == 0:
    #    code = run_container(buildmaster, rebuild("autogentoo/build-server"))
