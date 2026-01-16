#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

from songs import SONG_SIMPLE, SONG_TEST
from player import Player
from wireless import *

# This program is made for the second EV3 brick in the project showed on brick builds YouTube channel.

portlist = [Port.A, Port.B, Port.C, Port.D]
LOCAL_NOTES = [4, 5, 6, 7]  # Define which notes this EV3 can play

def main():
    ev3 = EV3Brick()
    ev3.screen.set_font(Font(size=50, bold=True))

    clock = StopWatch() # create clock

    client = Client(ev3, clock) # initialize bluetooth connection to server

    player = Player( # create player object to move motors
        ev3=ev3,
        clock=clock,
        local_notes=LOCAL_NOTES,
        portlist=portlist
    )

    while True:
        task = client.wait_for_task()
        print("Task recieved: ", task)

        if task in tasklist:
            if tasklist[task] == "TUNING MODE":
                ev3.screen.print("Tuning mode")
                selected_note_index = 0    
                while True:
                    note = client.wait_for_note()
                    print("Note recieved: ", note)
                    if note in LOCAL_NOTES:
                        player.play_note(note)
            elif tasklist[task] == "SONG MODE":
                # play song
                player.play(SONG_SIMPLE, clock.time())
        else:
            print("Unknown task received.")


main()