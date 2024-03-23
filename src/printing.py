"""
Print logging utilities.

Print statements have been inserted into other project modules 
in a way such that they are easy to remove without causing 
errors, but will probably never be removed.
"""

from pybricks.media.ev3dev import Font
from pybricks.tools import DataLog
from pybricks.hubs import EV3Brick

brick = None

data_log = DataLog("MESSAGE", name="roundabout_log", timestamp=False, extension="log")

text_width = 35

def break_line(line: str) -> str:
    i = 0
    l = len(line)
    while i < l:
        line = line[:i] + '\n' + line[i:]
        i += text_width
    return line

def set_screen(hub: EV3Brick):
    global brick
    brick = hub
    brick.screen.clear()
    brick.screen.set_font(Font(size=6))

def print_log(module_name: str, msg: str):
    s = "[LOG] (" + module_name + ") " + msg
    print(s)
    data_log.log(s)
    # brick.screen.print(break_line(s))

def print_warning(module_name: str, msg: str):
    s = "\033[38;5;214m[WARNING] (" + module_name + ") " + msg + "\033[m"
    print(s)
    brick.screen.print(break_line(s))
    data_log.log(s)

def print_error(module_name: str, msg: str):
    s = "\033[38;5;196m[ERROR] (" + module_name + ") " + msg + "\033[m"
    print(s)
    brick.screen.print(break_line(s))
    data_log.log(s)
