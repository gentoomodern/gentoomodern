#!/usr/bin/env python3

import re, docker
from .gentoomuch_common import image_tag_base, active_image_tag, profiles_amd64_cleaned

def get_active_stage():
    dckr = docker.from_env()
    for i in dckr.images.list():
        if active_image_tag in i.tags:
            if len(i.tags) == 2:
                for t in i.tags:
                    if not t == active_image_tag:
                        # TODO: Something
                        parser = tag_parser()
                        print(t)
                        parser.parse(t)
                        return parser
    exit("No active stage defined!")

class tag_parser:
    def __init__(self):
        self.arch = ''
        self.profile = ''
        self.stage_define = ''
        self.upstream = False

    def parse(self, tag):
        if tag == active_image_tag:
            return
        tag = re.sub(re.escape(image_tag_base), '', tag)
        self.upstream = False
        self.arch = tag[:tag.find('-')]
        tag = tag[tag.find('-') + 1:]
        print(tag)
        suffix = tag[tag.rfind(':') + 1:]
        self.upstream = bool(suffix == 'upstream')
        tag = tag[:tag.rfind(':')]
        print(tag)
        profile_found = False
        for p in profiles_amd64_cleaned:
            if tag.startswith(p):
                self.profile = p
                profile_found = True
                break
        if not profile_found:
            return
        tag = tag[len(self.profile) + 1:]
        print(tag)
        self.stage_define = tag # What's left over

    def arch(self):
        return self.arch

    def profile(self):
        return self.profile

    def stage_define(self):
        return self.stage_define

    def upstream(self):
        return self.upstream
