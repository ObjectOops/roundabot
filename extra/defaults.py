#!/usr/bin/env pybricks-micropython

from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

if __name__ == "__main__":
    left_motor = Motor(Port.D)
    right_motor = Motor(Port.B)
    steering_motor = Motor(Port.A)
    
    drive_base = DriveBase(left_motor, right_motor, 43, 170)
    straight_speed, straight_acceleration, turn_rate, turn_acceleration = drive_base.settings()

    dbd_speed, dbd_acceleration, _ = drive_base.distance_control.limits()
    dbd_pidf = drive_base.distance_control.pid()
    dbd_tolerance_speed, dbd_tolerance_position = drive_base.distance_control.target_tolerances()

    dbh_speed, dbh_acceleration, _ = drive_base.heading_control.limits()
    dbh_pidf = drive_base.heading_control.pid()
    dbh_tolerance_speed, dbh_tolerance_position = drive_base.heading_control.target_tolerances()

    lm_speed, lm_acceleration, _ = left_motor.control.limits()
    lm_pidf = left_motor.control.pid()
    lm_tolerance_speed, lm_tolerance_position = left_motor.control.target_tolerances()

    rm_speed, rm_acceleration, _ = right_motor.control.limits()
    rm_pidf = right_motor.control.pid()
    rm_tolerance_speed, rm_tolerance_position = right_motor.control.target_tolerances()

    st_speed, st_acceleration, _ = steering_motor.control.limits()
    st_pidf = steering_motor.control.pid()
    st_tolerance_speed, st_tolerance_position = steering_motor.control.target_tolerances()

    items = [
        ("Drive Base Straight Speed", straight_speed), 
        ("Drive Base Straight Acceleration", straight_acceleration), 
        ("Drive Base Turn Rate", turn_rate), 
        ("Drive Base Turn Acceleration", turn_acceleration), 
        ("Drive Base Speed", dbd_speed), 
        ("Drive Base Acceleration", dbd_acceleration), 
        ("Drive Base PIDF", dbd_pidf), 
        ("Drive Base Speed Tolerance", dbd_tolerance_speed), 
        ("Drive Base Position Tolerance", dbd_tolerance_position), 
        ("Left Motor Speed", lm_speed), 
        ("Left Motor Acceleration", lm_acceleration), 
        ("Left Motor PIDF", lm_pidf), 
        ("Left Motor Speed Tolerance", lm_tolerance_speed), 
        ("Left Motor Position Tolerance", lm_tolerance_position), 
        ("Right Motor Speed", rm_speed), 
        ("Right Motor Acceleration", rm_acceleration), 
        ("Right Motor PIDF", rm_pidf), 
        ("Right Motor Speed Tolerance", rm_tolerance_speed), 
        ("Right Motor Position Tolerance", rm_tolerance_position), 
        ("Steering Motor Speed", st_speed), 
        ("Steering Motor Acceleration", st_acceleration), 
        ("Steering Motor PIDF", st_pidf), 
        ("Steering Motor Speed Tolerance", st_tolerance_speed), 
        ("Steering Motor Position Tolerance", st_tolerance_position)
    ]

    for item in items:
        print(item[0], ":", item[1])
