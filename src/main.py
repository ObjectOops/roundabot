#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

import drivetrain

"""
Pseudo-code

(Also add test programs for manual control and default measuring.)

Do print debugs in case of runtime issue.
PIDF stuff.

Read and parse config file.
- Path to use.
- Color sensor activation.
- Front / back movements.
- Turn left / right movements.
- Color sensor trigger point.
Call drivetrain initialization function with configuration.
- Need formula for steering servo angle. Use gyro?
- Front / back with color sensor logic.

Read and parse movements file.

Print configuration info.
Calculate end coordinate.
Speak ready.

Wait for touch sensor to be actuated.

Follow movements. Call movement functions from drivetrain.
Color sensor movement function only uses the color sensor if it's active in config.

Remember to reset the encoders and related items on actual start up.

Configuration redundancy testing.
"""

# Create your objects here

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize a motor at port B.
test_motor = Motor(Port.S1)

# Write your program here

# Play a sound.
# ev3.speaker.beep()

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 90)

# Play another beep sound.

print('Hello, world!')

ev3.speaker.beep(frequency=1000, duration=500)

if __name__ == '__main__':
    print("Started.")
    drivetrain.test_func()
