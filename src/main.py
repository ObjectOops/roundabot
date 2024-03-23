#!/usr/bin/env pybricks-micropython

import sys

from pybricks.parameters import Port, Button
from pybricks.ev3devices import TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.tools import wait
import pybricks.media as brick

from configuration import Config, is_enabled
from drivetrain import Drivetrain
from path import Path, ActionType
from printing import *

do_not_wait = False

def prompt_continue():
    global do_not_wait
    print_log(__name__, "Waiting for continue...")
    pressed = None
    while not do_not_wait:
        pressed = ev3.buttons.pressed()
        if Button.CENTER in pressed or Button.DOWN in pressed:
            break
        wait(100)
    if Button.DOWN in pressed:
        sys.exit()
    while Button.CENTER in ev3.buttons.pressed():
        wait(100)

if __name__ == "__main__":
    ev3 = EV3Brick()
    set_screen(ev3)
    start_button = TouchSensor(Port.S1)

    ev3.screen.print("Roundabot has been started!")

    config = Config("/home/robot/roundabot/assets/config.txt")
    print_log(__name__, "Initialized configuration.")
    drivetrain = Drivetrain(config)
    print_log(__name__, "Initialized drivetrain.")
    path = Path({
        "i" : drivetrain.drive_forward, 
        "k" : drivetrain.drive_backward, 
        "j" : drivetrain.turn_left, 
        "l" : drivetrain.turn_right, 
        "ic" : drivetrain.drive_forward_color_sensor
    })
    print_log(__name__, "Initialized path.")
    path.load_path("/home/robot/roundabot/assets/paths/" + config.get_str("Run Path"))
    print_log(__name__, "Loaded path.")
    prompt_continue()

    show_these = [
        "*"
    ]
    for option in config._mapping:
        s = option + ": " + config._mapping[option]
        print_log(__name__, s)
        if show_these[0] == "*" or option in show_these:
            ev3.screen.print(s)

    prompt_continue()
    if is_enabled(config.get_str("Competition Mode")):
        field = [(i, j) for j in range(4) for i in range(4)]
        coords = path.calculate_coords(config.get_num("Start Coordinate X"), config.get_num("Start Coordinate Y"), {
            "i" : ActionType.FORWARDS, 
            "k" : ActionType.BACKWARDS, 
            "j" : ActionType.LEFT, 
            "l" : ActionType.RIGHT
        })
        tile = 20
        ev3.screen.clear()
        for x, y in field:
            ev3.screen.draw_box(x * tile, y * tile, x * tile + tile, y * tile + tile)
        for x, y in coords:
            y = 3 - y
            ev3.screen.draw_box(x * tile, y * tile, x * tile + tile, y * tile + tile, fill=True)
        prompt_continue()
    
    if config.redundant():
        print_warning(__name__, "Unused configuration options detected " + str(list(set(config._mapping.keys()).difference(config._used))))
    
    print_log(__name__, "Configuration complete.")
    ev3.speaker.set_speech_options(voice="f3", pitch=70)
    ev3.speaker.say("Waiting for touch sensor actuation.")

    while not start_button.pressed():
        wait(100)
    
    while not path.complete():
        action = path.next_action()

        action()
