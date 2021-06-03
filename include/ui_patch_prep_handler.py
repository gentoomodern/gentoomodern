#!/usr/bin/env python3

import re, os, sys
from .patches import prep_patch
from .gentoomuch_common import usage_str

force_arg_str       = '--force'
custom_repo_arg_str = '--custom-repo'
prep_str            = 'prep'
save_str            = 'save'
compile_str         = 'compile'


class ui_patch_prep_handler:
    
    def __init__(self, index : int):
        self.index              = index
        self.force              = False
        self.has_custom_repo    = False
        self.custom_repo        = ''
        self.name               = ''
        self.package            = ''
        self.version            = ''
    
    def handle(self):
        user_arg = sys.argv[self.index].strip()
        print("Handling arg = " + user_arg)
        while self.__is_optional_arg(user_arg):
            print("Handling arg = " + user_arg)
            user_arg = sys.argv[self.index].strip()
            self.__handle_optional_arg()
        indices_left = len(sys.argv) - self.index
        
        print('Arg length: ' + str(len(sys.argv)) + '. Indices left: ' + str(indices_left))
        print(sys.argv[indices_left:])
        # Our error message.
        usage_cmd_tail = ''
        if indices_left > 0:
            self.name = sys.argv[self.index].strip()
        else:
            exit('Need to set a patch name.')
        if indices_left > 1:
            self.package = sys.argv[self.index + 1].strip()
        else:
            exit("You need to set a package to patch!")
        if indices_left > 2:
            self.version = sys.argv[self.index + 2].strip()
            if self.__valid():
                prep_patch(self.name, self.package, self.version, bool(self.force), self.custom_repo)
            else:
                exit("ERROR in one of the arguments.")
        else:
            exit("Need to set a package version.")


    def __valid(self):
        if self.has_custom_repo == True:
            if self.custom_repo_name == '':
                exit("Custom repo needs a name!")
        if self.name == '':
            exit("Your patch needs a name!")
        if self.package == '':
            exit("Please set a package to patch.")
        if len(self.package.split('/')) == 0:
            exit("We need a fully-qualified package name. For example, sys-fs/lvm2 instead of lvm2.")
        if self.version == '':
            exit("Package version needs to be set.")
        return True

    def __get_custom_repo_name(self) -> str:
        self.index += 1
        return sys.argv[self.index].strip()

    def __is_optional_arg(self, arg) -> bool:
        return arg == force_arg_str or arg == custom_repo_arg_str
    
    def __handle_optional_arg(self):
        current_arg = sys.argv[self.index]
        if current_arg == force_arg_str:
            self.force = True
            self.index += 1
        elif current_arg == custom_repo_str:
            self.has_custom_repo = True
            self.custom_repo = self.__get_custom_repo_name()
            self.index += 1
        else:
            exit("Invalid option: " + current_arg)

    #def has_changed(self) -> bool:
    #    return False

    # opts = handle_optionals(index)
        # if opts[0] == True:
            # opts = handle_optionals(index, opts[1])
            # if opts[1][1] == True:
            # index += 1
        # if opts[0] == True:
            # opts == handle_optionals(index, opts[1])
            # index += 1
        # action = sys.argv[index + 2].strip()
        # if action == prep_str:
            # error_str += prep_str + ' '
            # if len(sys.argv) > index + 3:
                # patchname = sys.argv[index + 3].strip()
                # error_str += '<patch: ' + patchname + ' > '
                # print(error_str)
            # else:
                # print(error_str + ': Need to specify a name for your patch. Please retry.')
                # exit()
            # if len(sys.argv) > index + 4:
                # packagename = sys.argv[index + 4].strip()
                # error_str += '<package: ' + packagename + ' > '
                # print(error_str)
                # exit()
            # else:
                # print(error_str + ': Need to specify a package to patch.')
                # exit()
            # if len(sys.argv) > index + 5:
                # version = sys.argv[index + 5].strip()
                # error_str += '<version: ' + version + ' > '
                # print(prep_str + error_str)
                # exit()
            # else:
                # print(error_str + ": Must specify version to patch. Here they are:")
                # get_available_package_versions(packagename)
                # exit()
            # prep_patch(patchname, packagename, version, force, repo_name)
            # exit()
            # else:
                # print(usage + prep_str + ' <patch-name> <package> <version-str> [--force, --repo]')
                # exit()
