#!/usr/bin/env pybricks-micropython

# import termios
# import select
# import sys
# import os

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# original_state = None

# def stdin_immediate():
#     global original_state
#     if original_state is None:
#         original_state = termios.tcgetattr(sys.stdin)
#     new_state = termios.tcgetattr(sys.stdin)
#     new_state[3] &= ~termios.ICANON # No buffering.
#     new_state[3] &= ~termios.ECHO # Suppress echoing.
#     new_state[6][termios.VMIN] = 1
#     new_state[6][termios.VTIME] = 0
#     termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, new_state)

# def stdin_reset():
#     global original_state
#     if original_state is None:
#         print("Failed to reset terminal state.")
#         return
#     termios.tcsetattr(sys.stdin, termios.TCSANOW, original_state)
#     print("Reset terminal state.")

# def getch() -> str:
#     return str(os.read(sys.stdin.fileno(), 1), encoding="utf8")

# def kbhit() -> bool:
#     is_set, _, _ = select.select((sys.stdin), (), (), 0)
#     return sys.stdin in is_set

def rgb2hsv(r: float, g: float, b: float) -> tuple[float, float, float]:
    v = ma = max(r, g, b)
    mi = min(r, g, b)
    s = (ma - mi) / ma
    t = 0
    if ma == r:
        t = 0 + (g - b) / (ma - mi)
    elif ma == g:
        t = 2 + (b - r) / (ma - mi)
    elif ma == b:
        t = 4 + (r - g) / (ma - mi)
    h = 60 * t
    if h < 0:
        h += 360
    return (h, s, v)

if __name__ == "__main__":
    # stdin_immediate()

    left_motor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)
    right_motor = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    steering_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
    
    drive_base = DriveBase(left_motor, right_motor, 43, 170)

    color_sensor = ColorSensor(Port.S4)

    driving = False
    speed = 100
    turn = 25
    speed_map = {
        'w' : (speed, 0), 
        'a' : (0, -turn), 
        's' : (-speed, 0), 
        'd' : (0, turn)
    }
    while True:
        c = input()
        if c in "wasd" and len(c) != 0:
            if driving:
                drive_base.stop()
                driving = False
            else:
                driving = True
                if c in "ws":
                    steering_motor.track_target(0)
                    wait(250)
                if c == 'a':
                    steering_motor.track_target(-90)
                    wait(250)
                elif c == 'd':
                    steering_motor.track_target(90)
                    wait(250)
                print("Key:", c)
                speed, turn = speed_map[c]
                drive_base.drive(speed, turn)
        elif c == 'i':
            r, g, b = color_sensor.rgb()
            print("Position:", drive_base.distance(), "\nAngle:", drive_base.angle(), "\nColor Sensor:", (color_sensor.color(), color_sensor.ambient(), color_sensor.reflection(), color_sensor.rgb(), rgb2hsv(r, g, b)))
        elif c == 'q':
            drive_base.stop()
            wait(250)
            steering_motor.track_target(0)
            wait(250)
            break

    # stdin_reset()
