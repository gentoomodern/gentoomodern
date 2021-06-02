#!/usr/bin/env

import os
from .gentoomuch_common import 

# When you need files to persist, you cannot have them owned by root if you want to edit them.
# This method gives you the command needed to create a user (with an optionally-different group id) so that you get to come back to a fresh system, every time.
def get_useradd_str(username = 'gentoomuch-user'):
    return "useradd -u " + get_ + " -g " + username
