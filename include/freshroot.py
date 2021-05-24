#!/usr/bin/env python3

import os

def freshroot():
    os.chdir('work')
    os.system("docker-compose up --no-start && docker-compose run gentoomuch-builder /bin/bash")
