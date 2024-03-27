"""
Parses the robot's path from `assets/paths/` and performs additional calculations.
"""

from printing import *

class Path:

    def __init__(self, action_mapping: dict[str, bound_method | function]):
        self.action_mapping = action_mapping
        self.queue = []
        self.current = 0

    def load_path(self, file_path: str):
        with open(file_path, 'r') as fin:
            print_log(__name__, "Opened path file " + file_path + ".")
            lines = fin.readlines()
            for line in lines:
                segments = line.split(';')
                for segment in segments:
                    segment = segment.strip()
                    tokens = [token for token in segment.split(' ') if len(token) > 0]
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

                    if identifier not in self.action_mapping:
                        print_error(__name__, "Identifier \"" + identifier + "\" not found in action mapping.")
                    self.queue.append((identifier, self.action_mapping[identifier], arguments))
                    print_log(__name__, "Added action \"" + identifier + "\" with " + str(arguments) + " to queue.")

    def calculate_coords(self, x: int, y: int, action_type_mapping: dict[str, ActionType]) -> list[tuple[int, int]]:
        ret = [(x, y)]
        heading = 0
        for identifier, _, args in self.queue:
            if identifier not in action_type_mapping:
                print_log(__name__, "Action \"" + identifier + "\" not found in action type mapping.")
                continue
            delta = action_type_mapping[identifier]
            if len(delta) != 3:
                print_warning(__name__, "Delta " + str(delta) + " does not have a length of 3.")
            if delta == ActionType.LEFT:
                heading -= 90
            elif delta == ActionType.RIGHT:
                heading += 90
            
            iterations = 1
            if delta == ActionType.FORWARDS or delta == ActionType.BACKWARDS:
                iterations = args[0] if len(args) > 0 else 1

            for i in range(iterations):
                dx, dy = self.rotate(delta, self.angle_wrap(heading) / 90)
                x += dx
                y += dy
                ret.append((x, y))
                print_log(__name__, "Added coordinate " + str((x, y)) + ".")
        return ret

    def angle_wrap(self, degrees: float) -> float:
        while degrees < 0 or degrees >= 360:
            if degrees < 0:
                degrees += 360
            elif degrees >= 360:
                degrees -= 360
        return degrees
    
    def rotate(self, movement: tuple[float, float], positive_nineties: int) -> tuple[float, float]:
        dx, dy, _ = movement
        while positive_nineties > 0:
            temp = dx
            dx = dy
            dy = -temp
            positive_nineties -= 1
        return (dx, dy)

    def complete(self) -> bool:
        return len(self.queue) == 0

    def next_action(self) -> tuple[str, bound_method | function, list[float]]:
        try:
            print_log(__name__, "Popped action \"" + self.queue[0][0] + "\" \"" + self.queue[0][1].__name__ + "\" " + str(self.queue[0][2]) + ".")
        except AttributeError:
            print_log(__name__, "Popped action \"" + self.queue[0][0] + "\" \""  + str(self.queue[0][1]) + "\" " + str(self.queue[0][2]) + ".")
        return self.queue.pop(0)

class ActionType():
    FORWARDS = (0, 1, 0)
    BACKWARDS = (0, -1, 0)
    LEFT = (0, 1, 1)
    RIGHT = (0, 1, 2)
