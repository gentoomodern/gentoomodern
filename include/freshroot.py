#!/usr/bin/env python3

import os

def freshroot():
    os.system("docker-compose down & docker-compose down & docker-compose up --no-start && docker-compose run gentoomuch-builder /bin/bash")
