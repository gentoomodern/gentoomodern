#!/usr/bin/env python3

import docker
from .gentoomuch_common import image_tag_base, current_image_tag

def get_current_stage():
    dckr = docker.from_env()
    for i in dckr.images.list():
        print('IMAGE')
        print(i.id)
        for t in i.tags:
            print(t)
        print()
    return []

def set_current_stage():
    os.cmd('docker rmi ' + current_image_tag)
    os.cmd()

def sanitize_stages():
    

#def get_current_stage():
    

#def get_current_profile():
    
