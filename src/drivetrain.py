"""
The Drivetrain.

Since the robot is designed to only turn around one of the 
powered wheels as a pivot, the Pybricks DriveBase turning 
will not be used.
"""

from enum import Enum, auto

from printing import *
from configuration import Config

class Drivetrain:

    def __init__(self, config: Config):
        if (cs := config.get_str("Color Sensor")) != "enabled" and cs != "disabled":
            print_warning(__name__, "Invalid value for \"Color Sensor\". Falling back to disabled.")
        self.color_sensor_enabled = config.get_str("Color Sensor") == "enabled"
        
        self.target_position_tolerance = config.get_num("Target Position Tolerance")
        self.speed_tolerance = config.get_num("Target Speed Tolerance")
        
        self.straight_speed = config.get_num("Straight Speed")
        self.straight_acceleration = config.get_num("Straight Acceleration")
        self.turn_rate = config.get_num("Turn Rate")
        self.turn_acceleration = config.get_num("Turn Acceleration")
        
        self.dpid_Kp = config.get_num("Drive PID Kp")
        self.dpid_Ki = config.get_num("Drive PID Ki")
        self.dpid_Kd = config.get_num("Drive PID Kd")
        self.dpid_Kf = config.get_num("Drive PID Kf")
        self.dpid_ir = config.get_num("Drive PID Integral Rate")
        self.dpid_lm = config.get_num("Drive PID Integral Limit")

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
        
        self.tr_outer_delta = config.get_num("Turn Right Outer Delta")
        self.tr_inner_delta = config.get_num("Turn Right Inner Delta")
        self.tl_outer_delta = config.get_num("Turn Left Outer Delta")
        self.tl_inner_delta = config.get_num("Turn Left Inner Delta")

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

class ColorSensorMode(Enum):
    BASIC_COLOR = auto()
    AMBIENT = auto()
    REFLECTION = auto()
    HUE = auto()
