#!/usr/bin/env python3

from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_dockerized_profile_name import get_dockerized_profile_name


def get_dockerized_name(arch, profile, stage, upstream):
    return "stage3-" + arch + "-" + get_dockerized_profile(profile) + ("" if upstream else "-" + get_dockerized_stagedef_name(stage))
