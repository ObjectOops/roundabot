import termios
import select
import sys
import os

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.robotics import DriveBase
from pybricks.parameters import Port
from pybricks.tools import wait

original_state = None

def stdin_immediate():
    global original_state
    if original_state is None:
        original_state = termios.tcgetattr(sys.stdin)
    new_state = termios.tcgetattr(sys.stdin)
    new_state[3] &= ~termios.ICANON # No buffering.
    new_state[3] &= ~termios.ECHO # Suppress echoing.
    new_state[6][termios.VMIN] = 1
    new_state[6][termios.VTIME] = 0
    termios.tcsetattr(sys.stdin, termios.TCSANOW, new_state)

def stdin_reset():
    global original_state
    if original_state is None:
        print("Failed to reset terminal state.")
        return
    termios.tcsetattr(sys.stdin, termios.TCSANOW, original_state)
    print("Reset terminal state.")

def getch() -> str:
    return str(os.read(sys.stdin.fileno(), 1), encoding="utf8")

def kbhit() -> bool:
    is_set, _, _ = select.select((sys.stdin), (), (), 0)
    return sys.stdin in is_set

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
    stdin_immediate()

    left_motor = Motor(Port.D)
    right_motor = Motor(Port.A)
    steering_motor = Motor(Port.B)
    
    drive_base = DriveBase(left_motor, right_motor, 50, 10)

    color_sensor = ColorSensor(Port.S1)

    driving = False
    speed = 5
    turn = 5
    while True:
        c = getch() if kbhit() else None
        match c:
            case 'w', 'a', 's', 'd':
                if driving:
                    drive_base.stop()
                    driving = False
                else:
                    driving = True
            case 'w', 's':
                steering_motor.track_target(0)
                wait(250)
            case 'a', 'd':
                steering_motor.track_target(90)
                wait(250)
            case 'w':
                drive_base.drive(speed, 0)
            case 'a':
                drive_base.drive(0, -turn)
            case 's':
                drive_base.drive(-speed, 0)
            case 'd':
                drive_base.drive(0, turn)
            case 'i':
                print(f"Position: {drive_base.position()}\nAngle: {drive_base.angle()}\nColor Sensor: {(color_sensor.color(), color_sensor.ambient(), color_sensor.reflection(), color_sensor.rgb(), rgb2hsv(color_sensor.rgb()))}")
            case 'q':
                break

    stdin_reset()
