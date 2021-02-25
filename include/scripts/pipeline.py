#!/usr/bin/env python3

import os


buildmaster = 'autogentoo-builder'
#packager = "autogentoo-packager"
package_host = "autogentoo-package-host"
git_worker = "autogentoo-git-worker"
sync = "emerge --sync"

rebuild_emptytree = "emerge -uDkq --changed-use --emptytree @world"

def run_container(root, command):
    return os.system("docker-compose run " + root + " " + command)

def create_mutable_container(root, name):
    # TODO:
    # Make temp Dockerfile
    # Build our Dockerfile
    # Assign the name
    return os.system()

def checkout_config(branch):
    return os.system("git -C config/autogentoo-builder checkout " + branch)

def build(packageset):
    return "emerge -uDkq --changed-use @" + packageset

def install(packageset):
    return "FEATURES='usepkgonly' " + build(packageset)


#TODO: Optimize into a single docker-compose run
# We run the initial bootstrap
#if code == 0:
#prep_config()
code = checkout_config("bootstrap")
code = run_container(buildmaster, rebuild_emptytree)#"bash -c '" + sync + " && " + rebuild_emptytree + "'")

# We can now recompile libcap with its default options again.
if code == 0:
    code = checkout_config("bootstrap-2")
    code = run_container(buildmaster, build("autogentoo/build-server"))
    #if code == 0:
    #    code = run_container(buildmaster, rebuild("autogentoo/build-server"))


code = os.system('rm -rf ./build/*')
