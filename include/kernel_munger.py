#!/usr/bin/env python3


class kernel_munger:

    def __init__(self):
        self.variables_to_values = {} # str:str

    def munge(self, kconf_path: str) -> bool:
        f = open(kconf_path, 'r')
        ctr = 0
        while True:
            line_str = f.readline().strip()
            # Stops the charade when there's no line to put in anymore.
            if not line_str:
                break
            # Ignore comments.
            if line_str[0] == '#':
                continue
            parts = line_str.split('=')
            # This would imply only a variable without a value assigned.
            if len(parts) < 2:
                print("Invalid Kernel config at line " + ctr + " -> " + line_str)
                return False
            # The following would mean that there is another = sign in the value that is being assigned.
            # For example, it can happen in the case of a built-in command.
            elif len(parts) > 2:
                key   = parts[0]
                value = ''
                for v in parts[1:]:
                    value += v
            # Now we are left with the base-case: A variable and a value.
            else:
                key   = parts[0]
                value = parts[1]
            if key in self.variables_to_values and self.variables_to_values[key] != value:
                print("Existing variable " + key + " in kernel config, with a different value than the one being assigned.")
            self.variables_to_values[key] = value
            ctr += 1
            f.close()
            return True

    def writeout(self, output_file: str):
        f = open(output_file, 'w')
        for k, v in self.variables_to_values:
            f.writeline(k + '=' + v + '\n')
