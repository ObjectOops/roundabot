"""
Parses the robot's path from `assets/paths/` and performs additional calculations.
"""

from printing import *

class Path:

    def __init__(self, action_mapping: dict[str, function]):
        self.action_mapping = action_mapping
        self.queue = []
        self.current = 0

    def load_path(self, file_path: str):
        with open(file_path, 'r') as fin:
            print_log(__name__, "Opened path file " + file_path + ".")
            lines = fin.readlines()
            identifiers = [token.strip() for token in line.split(';') for line in lines]
            for identifier in identifiers:
                if identifier not in self.action_mapping:
                    print_error(__name__, "Identifier \"" + identifier + "\" not found in action mapping.")
                self.queue.append(self.action_mapping[identifer])
                print_log(__name__, "Added action \"" + identifier + "\" to queue.")
            
    def calculate_coords(self, x: int, y: int, action_type_mapping: dict[str, ActionType]) -> list[tuple[int, int]]:
        ret = []
        for action in queue:
            if action not in action_type_mapping:
                print_log(__name__, "Action \"" + action + "\" not found in action type mapping.")
                continue
            delta = action_type_mapping[action]
            if len(delta) != 2:
                print_warning(__name__, "Delta " + delta + " does not have a length of 2.")
            dx, dy = delta
            x += dx
            y += dy
            ret.append((x, y))
            print_log(__name__, "Added coordinate " + (x, y) + ".")
        return ret

    def complete(self) -> bool:
        return len(self.queue) == 0

    def next_action(self) -> function:
        print_log(__name__, "Popped action \"" + self.queue[len(self.queue) - 1].__name__ + "\".")
        return self.queue.pop(len(self.queue) - 1)

class ActionType():
    FORWARDS = (0, 1)
    BACKWARDS = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
