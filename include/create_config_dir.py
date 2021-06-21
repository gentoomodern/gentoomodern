#!/usr/bin/env python3

import os


def create_config_dir(path) -> bool:
        if os.isfile(path):
            print("Need to specify directory at " + path + ' and got a file instead.')
            return False
        elif os.isdir(path) and len(os.listdir(path)) > 0:
            print(path + " needs to be an empty directory.")
            return False
        else:
            for d in ('buildhook.defines', 'buildhook.frags', 'cpu.frags', 'kconf.frags', 'kernel.defines', 'package.sets', 'patch.diffs', 'patch.profiles', 'portage.frags', 'stage.defines', 'system.defines'):
                os.makedirs(os.path.join(path, d), exist_ok = True)
                if d == 'buildhook.frags':
                    for dd in ('0-copy', '1-premerge', '2-unmerge', '3-postmerge', '4-services', '5-remove')
                        os.makedirs(os.path.join(path, d, dd), exist_ok = True)
            return True
