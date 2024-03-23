"""
Print logging utilities.

Print statements have been inserted into other project modules 
in a way such that they are easy to remove without causing 
errors, but will probably never be removed.
"""

import pybricks.media as brick

def print_log(module_name: str, msg: str):
    s = "[LOG] (" + module_name + ") " + msg
    print(s, flush=True)
    # brick.print(s)

def print_warning(module_name: str, msg: str):
    s = "\033[38;5;214m[WARNING] (" + module_name + ") " + msg + "\033[m"
    print(s, flush=True)
    brick.print(s)

def print_error(module_name: str, msg: str):
    s = "\033[38;5;196m[ERROR] (" + module_name + ") " + msg + "\033[m"
    print(s, flush=True)
    brick.print(s)
