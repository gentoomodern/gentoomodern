#!/usr/bin/env python3

import os, docker

def dockerfile_build(arch, profile, stagedef, upstream = False):
    
