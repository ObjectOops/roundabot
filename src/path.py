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
                segments = line.split(';')
                for segment in segments:
                    segment = segment.strip()
                    tokens = segment.split(' ')
                    tokens = [token for token in tokens if len(token) > 0]
                    if len(tokens) == 0:
                        continue

                    identifier = tokens[0]
                    arguments = []
                    token_len = len(tokens)

                    # For the purposes of this project, attempting to cast all arguments to floats suffices.
                    for i in range(1, token_len):
                        try:
                            float(tokens[i])
                        except:
                            print_error(__name__, "Argument is not a float \"" + tokens[i] + "\" in " + str(tokens) + ".")
                        arguments.append(float(tokens[i]))

                    self.identifiers.append(identifier)
                    if identifier not in self.action_mapping:
                        print_error(__name__, "Identifier \"" + identifier + "\" not found in action mapping.")
                    self.queue.append((self.action_mapping[identifier], arguments))
                    print_log(__name__, "Added action \"" + identifier + "\" with " + str(arguments) + " to queue.")

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

    def next_action(self) -> tuple[bound_method | function, list[float]]:
        try:
            print_log(__name__, "Popped action \"" + self.queue[0][0].__name__ + "\".")
        except AttributeError:
            print_log(__name__, "Popped action \"" + str(self.queue[0][0]) + "\".")
        return self.queue.pop(0)

class ActionType():
    FORWARDS = (0, 1)
    BACKWARDS = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
