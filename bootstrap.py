#!/usr/bin/env python3

import os

from common import prep_config

prep_config()

os.system('docker-compose up')
