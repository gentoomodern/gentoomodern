#!/usr/bin/env

import os
from .gentoomodern_common import 

# When you need files to persist, you cannot have them owned by root if you want to edit them.
# This method gives you the command needed to create a user (with an optionally-different group id) so that you get to come back to a fresh system, every time.
def get_useradd_str(uid: int = 1000, username = 'gentoomodern-user'):
    return "useradd -u " + uid + " -g " + username
