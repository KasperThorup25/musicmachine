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

def main():
    ev3 = EV3Brick()
    ev3.screen.set_font(Font(size=30, bold=False))

    clock = StopWatch()

    server = Server(ev3, clock)

    player = Player(
        ev3=ev3,
        clock=clock,
        local_notes=LOCAL_NOTES,
        portlist=portlist
    )

    selected_note_index = 0    

    wait(200)
    server.send_task(1) # send tuning mode task to the other ev3
    wait(200)

    while True:
        ev3.screen.print("Tuning mode")
        ev3.screen.print("Note:", selected_note_index)
        if Button.CENTER in ev3.buttons.pressed():
            if selected_note_index in LOCAL_NOTES:
                player.play_note(LOCAL_NOTES[selected_note_index])
            else:
                # send note to other ev3
                server.send_note(selected_note_index)
            while Button.CENTER in ev3.buttons.pressed():
                pass
        if Button.LEFT in ev3.buttons.pressed():
            # previous note
            selected_note_index -= 1
            if selected_note_index < 0:
                selected_note_index = len(ALL_NOTES) - 1
            while Button.LEFT in ev3.buttons.pressed():
                pass
        if Button.RIGHT in ev3.buttons.pressed():
            # next note
            selected_note_index += 1
            if selected_note_index >= len(ALL_NOTES):
                selected_note_index = 0
            while Button.RIGHT in ev3.buttons.pressed():
                pass
        wait(50)
        ev3.screen.clear()

main()