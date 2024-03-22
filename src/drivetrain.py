"""
The Drivetrain.

Since the robot is designed to use either the left or right wheel
as a pivot when turning left or right, the Pybricks DriveBase turning 
is a secondary feature.
"""

from enum import Enum, auto
import math

from pybricks.parameters import Direction, Port, Color
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.tools import StopWatch, wait
from pybricks.robotics import DriveBase

from configuration import Config
from printing import *
from filter import *

class Drivetrain:

    def __init__(self, config: Config):
        self.left_motor = Motor(Port.D, positive_direction=self.left_motor_direction)
        self.right_motor = Motor(Port.A, position_direction=self.right_motor_direction)
        self.steering_motor = Motor(Port.B, positive_direction=self.steering_motor_direction)
        self.drive_base = DriveBase(self.left_motor, self.right_motor, self.wheel_diameter, self.track_width)
        self.color_sensor = ColorSensor(Port.S1)
    
        self.wheel_diameter = config.get_num("Wheel Diameter")
        self.turn_steering_angle = config.get_num("Turn Steering Angle")
        self.turn_wait = config.get_num("Turn Wait")
        self.cycle_wait = config.get_num("Cycle Wait")
        self.move_timeout = config.get_num("Move Timeout")

        self.color_sensor_enabled = is_enabled(config.get_str("Color Sensor"))
        
        self.distance_tolerance_defaults = is_enabled(config.get_str("Use Distance Tolerance Defaults"))
        self.heading_tolerance_defaults = is_enabled(config.get_str("Use Heading Tolerance Defaults"))
        dtd_speed, dtd_position = self.drive_base.distance_control.target_tolerances()
        htd_speed, htd_position = self.drive_base.heading_control.target_tolerances()
        if self.distance_tolerance_defaults:
            self.distance_position_tolerance = dtd_position
            self.distance_speed_tolerance = dtd_speed
        else:
            self.distance_position_tolerance = config.get_num("Target Distance Position Tolerance")
            self.distance_speed_tolerance = config.get_num("Target Distance Speed Tolerance")
        if self.heading_tolerance_defaults:
            self.heading_position_tolerance = htd_position
            self.heading_speed_tolerance = htd_speed
        else:
            self.heading_position_tolerance = config.get_num("Target Heading Position Tolerance")
            self.heading_speed_tolerance = config.get_num("Target Heading Speed Tolerance")
        
        self.kinematic_defaults = is_enabled(config.get_str("Use Kinematic Defaults"))
        kin_sp, kin_sa, kin_tr, kin_ta = self.drive_base.settings()
        if self.kinematic_defaults:
            self.straight_speed = kin_sp
            self.straight_acceleration = kin_sa
            self.turn_rate = kin_tr
            self.turn_acceleration = kin_ta
        else:
            self.straight_speed = config.get_num("Straight Speed")
            self.straight_acceleration = config.get_num("Straight Acceleration")
            self.turn_rate = config.get_num("Turn Rate")
            self.turn_acceleration = config.get_num("Turn Acceleration")
        
        self.dpid_defaults = is_enabled(config.get_str("Use Drive PID Defaults"))
        ddp, ddi, ddd, ddlm, ddir, ddf = self.drive_base.distance_control.pid()
        if self.dpid_defaults:
            self.dpid_Kp = ddp
            self.dpid_Ki = ddi
            self.dpid_Kd = ddd
            self.dpid_Kf = ddf
            self.dpid_ir = ddir
            self.dpid_lm = ddlm
        else:
            self.dpid_Kp = config.get_num("Drive PID Kp")
            self.dpid_Ki = config.get_num("Drive PID Ki")
            self.dpid_Kd = config.get_num("Drive PID Kd")
            self.dpid_Kf = config.get_num("Drive PID Kf")
            self.dpid_ir = config.get_num("Drive PID Integral Rate")
            self.dpid_lm = config.get_num("Drive PID Integral Limit")

        self.tpid_defaults = is_enabled(config.get_str("Use Turn PID Defaults"))
        tdp, tdi, tdd, tdlm, tdir, tdf = self.drive_base.distance_control.pid()
        if self.tpid_defaults:
            self.tpid_Kp = tdp
            self.tpid_Ki = tdi
            self.tpid_Kd = tdd
            self.tpid_Kf = tdf
            self.tpid_ir = tdir
            self.tpid_lm = tdlm
        else:
            self.tpid_Kp = config.get_num("Turn PID Kp")
            self.tpid_Ki = config.get_num("Turn PID Ki")
            self.tpid_Kd = config.get_num("Turn PID Kd")
            self.tpid_Kf = config.get_num("Turn PID Kf")
            self.tpid_ir = config.get_num("Turn PID Integral Rate")
            self.tpid_lm = config.get_num("Turn PID Integral Limit")

        self.track_width = config.get_num("Track Width")

        self.forward_delta = config.get_num("Forward Delta")
        self.backward_delta = config.get_num("Backward Delta")
        if self.forward_delta - self.backward_delta >= 0.1 * 0.5 * (self.forward_delta + self.backward_delta):
            print_warning(__name__, "Forward and backward deltas are too far apart.")
        
        self.tl_outer_delta = config.get_num("Turn Left Outer Delta")
        self.tl_inner_delta = config.get_num("Turn Left Inner Delta")
        self.tr_outer_delta = config.get_num("Turn Right Outer Delta")
        self.tr_inner_delta = config.get_num("Turn Right Inner Delta")

        self.turn_forward_delta = config.get_num("Turn Forward Delta")

        csm = config.get_str("Color Sensor Trigger Type")
        valid_color_sensor_modes = {
            "color" : (ColorSensorMode.BASIC_COLOR, "Null"), 
            "ambient" : (ColorSensorMode.AMBIENT, "Color Sensor Trigger Ambient Delta"), 
            "reflection" : (ColorSensorMode.REFLECTION, "Color Sensor Trigger Reflection Delta"), 
            "hue" : (ColorSensorMode.HUE, "Color Sensor Trigger Hue Delta")
        }
        if csm not in valid_color_sensor_modes:
            print_error(f"Invalid color sensor trigger type \"{csm}\".")
        self.color_sensor_mode = valid_color_sensor_modes[csm]

        self.color_sensor_pre_forward_delta = config.get_num("Color Sensor Pre Forward Delta")
        self.color_sensor_forward_delta = config.get_num("Color Sensor Forward Delta")
        self.color_sensor_backward_delta = config.get_num("Color Sensor Backward Delta")

        self.left_motor_direction = get_direction(config.get_str("Left Motor Direction"))
        self.right_motor_direction = get_direction(config.get_str("Right Motor Direction"))
        self.steering_motor_direction = get_direction(config.get_str("Steering Motor Direction"))

        self.drive_base.settings(self.straight_speed, self.straight_acceleration, self.turn_rate, self.turn_acceleration)
        # _, _, left_actuation = self.left_motor.limits()
        # self.left_motor.control.limits(self.straight_speed, self.straight_acceleration, left_actuation)
        # _, _, right_actuation = self.right_motor.limits()
        # self.right_motor.control.limits(self.straight_speed, self.straight_acceleration, right_actuation)

        self.drive_base.distance_control.pid(self.dpid_Kp, self.dpid_Ki, self.dpid_Kd, self.dpid_lm, self.dpid_ir, self.dpid_Kf)

        self.drive_base.heading_control.pid(self.tpid_Kp, self.tpid_Ki, self.tpid_Kd, self.tpid_lm, self.tpid_ir, self.tpid_Kf)
        # self.left_motor.control.pid(self.tpid_Kp, self.tpid_Ki, self.tpid_Kd, self.tpid_lm, self.tpid_ir, self.tpid_Kf)
        # self.right_motor.control.pid(self.tpid_Kp, self.tpid_Ki, self.tpid_Kd, self.tpid_lm, self.tpid_ir, self.tpid_Kf)

        self.drive_base.distance_control.target_tolerances(self.distance_speed_tolerance, self.distance_position_tolerance)

        self.drive_base.heading_control.target_tolerances(self.heading_speed_tolerance, self.heading_position_tolerance)
        # self.left_motor.target_tolerances(self.heading_speed_tolerance, self.heading_position_tolerance)
        # self.right_motor.target_tolerances(self.heading_speed_tolerance, self.heading_position_tolerance)

        self.left_motor.stop()
        self.right_motor.stop()
        self.drive_base.stop()
        
    def is_enabled(s: str) -> bool:
        if s != "enabled" and s != "disabled":
            print_warning(__name__, f"Invalid boolean value \"{s}\". Falling back to disabled.")
        return s == "enabled"

    def get_direction(s: str) -> Direction:
        if s != "forward" and s != "reverse":
            print_warning(__name__, f"Invalid direction value \"{s}\". Falling back to forward.")
        return Direction.CLOCKWISE if s == "forward" else Direction.COUNTERCLOCKWISE
    
    def drive_forward(self):
        self.steering_motor.track_target(0)
        wait(self.turn_wait)
        self.drive_base.straight(self.forward_delta)
    
    def drive_forward_color_sensor(self):
        color_sensor_generator = test_color_sensor()
        self.steering_motor.track_target(0)
        wait(self.turn_wait)
        self.drive_base.straight(self.color_sensor_pre_forward_delta)
        target_distance = self.drive_base.distance() + self.color_sensor_forward_delta
        timer = StopWatch()
        while abs(err := self.drive_base.distance() - target_distance) > self.distance_position_tolerance and timer.time() < self.move_timeout:
            self.drive_base.drive(err * self.dpid_Kp, 0)
            if next(color_sensor_generator):
                print_log(__name__, f"Color sensor detected target point.")
                self.drive_base.straight(-self.color_sensor_backward_delta)
                break
            wait(self.cycle_wait)
    
    def test_color_sensor(self) -> bool:
        match self.color_sensor_mode[0]:
            case ColorSensorMode.BASIC_COLOR:
                initial_color = self.color_sensor.color()
                while True:
                    yield self.color_sensor.color() != initial_color
            case ColorSensorMode.AMBIENT:
                initial_ambience = self.color_sensor.ambient()
                while True:
                    yield abs(self.color_sensor.ambient() - initial_ambience) >= self.color_sensor_mode[1]
            case ColorSensorMode.REFLECTION:
                initial_reflection = self.color_sensor.reflection()
                while True:
                    yield abs(self.color_sensor.reflection() - initial_reflection) >= self.color_sensor_mode[1]
            case ColorSensorMode.HUE:
                r, g, b = self.color_sensor.rgb()
                initial_hue = rgb2hsv(r, g, b)[0]
                while True:
                    r, g, b = self.color_sensor.rgb()
                    yield abs(rgb2hsv(r, g, b)[0] - initial_hue) >= self.color_sensor_mode[1]

    def drive_backward():
        self.steering_motor.track_target(0)
        wait(self.turn_wait)
        self.drive_base.straight(-self.backward_delta)
    
    def turn_left():
        self.drive_base.stop()
        self.steering_motor.track_target(self.turn_steering_angle)
        wait(self.turn_wait)
        
        heading = self.drive_base.angle()
        target_heading = heading - 90
        left = self.left_motor.angle() / 180 * math.pi * self.wheel_diameter / 2
        original_left = left + self.tl_inner_delta
        right = self.right_motor.angle() / 180 * math.pi * self.wheel_diameter / 2
        timer = StopWatch()
        while abs(err := heading - target_heading) > self.heading_position_tolerance and timer.time() < self.move_timeout:
            heading, left, right = calculate_heading_manual(heading, left, right)
            self.right_motor.run(err * self.tpid_Kp)
            self.left_motor.run((original_left - left) * self.dpid_Kp)
            wait(self.cycle_wait)
        
        # Alternatively, just run to a predetermined value.
        # self.left_motor.hold()
        # self.right_motor.run_angle(self.straight_speed, self.tl_outer_delta)

        self.drive_base.straight(self.turn_forward_delta)

    def turn_right():
        self.drive_base.stop()
        self.steering_motor.track_target(self.turn_steering_angle)
        wait(self.turn_wait)
        
        heading = self.drive_base.angle()
        target_heading = heading + 90
        left = self.left_motor.angle() / 180 * math.pi * self.wheel_diameter / 2
        right = self.right_motor.angle() / 180 * math.pi * self.wheel_diameter / 2
        original_right = right + self.tr_inner_delta
        timer = StopWatch()
        while abs(err := heading - target_heading) > self.heading_position_tolerance and timer.time() < self.move_timeout:
            heading, left, right = calculate_heading_manual(heading, left, right)
            self.left_motor.run(err * self.tpid_Kp)
            self.right_motor.run((original_right - right) * self.dpid_Kp)
            wait(self.cycle_wait)
        
        # Alternatively, just run to a predetermined value.
        # self.right_motor.hold()
        # self.left_motor.run_angle(self.straight_speed, self.tr_outer_delta)

        self.drive_base.straight(self.turn_forward_delta)
    
    def calculate_heading_manual(heading_previous, left_previous: float, right_previous: float) -> tuple[float, float, float]:
        # Reference: https://github.com/8696-Trobotix/mollusc/blob/03b87be3b62fa3d2800822e34b83919a329c2cbc/auto/odometry/DeadWheels.java
        dl = self.left_motor.angle() / 180 * math.pi * self.wheel_diameter / 2 - left_previous
        dr = self.right_motor.angle() / 180 * math.pi * self.wheel_diameter / 2 - right_previous
        dh = (dl - dr) / self.track_width
        return (heading_previous + dh, left_previous + dl, right_previous + dr)

    def turn_in_place(angle: float):
        self.steering_motor.track_target(90 * math.copysign(1, angle))
        wait(self.turn_wait)
        self.drive_base.turn(angle)

class ColorSensorMode(Enum):
    BASIC_COLOR = auto()
    AMBIENT = auto()
    REFLECTION = auto()
    HUE = auto()
