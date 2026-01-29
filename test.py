#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, NumericMailbox

import urandom
from random import randint
import threading

from songs import songs
from player import Player
from wireless import Server

portlist = [Port.A, Port.B, Port.C, Port.D]
LOCAL_NOTES = [0, 1, 2, 3]  # Define which notes this EV3 can play
ALL_NOTES = [0, 1, 2, 3, 4, 5, 6, 7]

# same function as in player.py to run the motor
def run_motor(ev3, motor):
        motor.dc(100) #move motor at 100% speed
        wait(40)
        motor.hold() # hold position after 40 ms
        motor.run_target(-500, 0, then=Stop.HOLD, wait=True) # return to 0 position
        return

def main():
    ev3 = EV3Brick()
    wait(2000)

    # setup motor
    motor = Motor(Port.D)
    motor.control.target_tolerances(speed=500, position=1)
    motor.run_until_stalled(-100, duty_limit=10) # Move motor until endstop
    motor.reset_angle(0) # Reset angle to zero

    while True:
        if Button.CENTER in ev3.buttons.pressed():
            run_motor(ev3, motor)
        wait(50)

main()