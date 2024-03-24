"""
Parses the robot's path from `assets/paths/` and performs additional calculations.
"""

from printing import *

class Path:

    def __init__(self, action_mapping: dict[str, bound_method | function]):
        self.action_mapping = action_mapping
        self.queue = []
        self.identifiers = []
        self.current = 0

    def load_path(self, file_path: str):
        with open(file_path, 'r') as fin:
            print_log(__name__, "Opened path file " + file_path + ".")
            lines = fin.readlines()
            for line in lines:
                tokens = line.split(';')
                for token in tokens:
                    self.identifiers.append(token.strip())
            for identifier in self.identifiers:
                if identifier not in self.action_mapping:
                    print_error(__name__, "Identifier \"" + identifier + "\" not found in action mapping.")
                self.queue.append(self.action_mapping[identifier])
                print_log(__name__, "Added action \"" + identifier + "\" to queue.")
            
    def calculate_coords(self, x: int, y: int, action_type_mapping: dict[str, ActionType]) -> list[tuple[int, int]]:
        ret = [(x, y)]
        for identifier in self.identifiers:
            if identifier not in action_type_mapping:
                print_log(__name__, "Action \"" + identifier + "\" not found in action type mapping.")
                continue
            delta = action_type_mapping[identifier]
            if len(delta) != 2:
                print_warning(__name__, "Delta " + delta + " does not have a length of 2.")
            dx, dy = delta
            x += dx
            y += dy
            ret.append((x, y))
            print_log(__name__, "Added coordinate " + str((x, y)) + ".")
        return ret

    def complete(self) -> bool:
        return len(self.queue) == 0

    def prepare(self):
        self.queue.reverse()

    def next_action(self) -> bound_method | function:
        try:
            print_log(__name__, "Popped action \"" + self.queue[len(self.queue) - 1].__name__ + "\".")
        except AttributeError:
            print_log(__name__, "Popped action \"" + str(self.queue[len(self.queue) - 1]) + "\".")
        return self.queue.pop(len(self.queue) - 1)

class ActionType():
    FORWARDS = (0, 1)
    BACKWARDS = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
