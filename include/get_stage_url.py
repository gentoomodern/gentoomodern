#!/usr/bin/env python3

from .get_cleaned_profile import get_cleaned_profile


def get_stage_url(arch, profile):
    head = "https://ftp-osl.osuosl.org/pub/gentoo/releases/"
    tail = "/autobuilds/"
    return head + arch + tail + get_cleaned_profile(profile)
