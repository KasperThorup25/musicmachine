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
    ev3.screen.set_font(Font(size=20, bold=False))

    clock = StopWatch()

    server = Server(ev3, clock)

    player = Player(
        ev3=ev3,
        clock=clock,
        local_notes=LOCAL_NOTES,
        portlist=portlist
    )

    wait(200)
    server.send_task(0) # send song mode task to the other ev3
    wait(200)
    
    play_delay = 1000 # play song 1 second delayed
    selected_song_index = 0
    while True:
        ev3.screen.print("Song mode")
        ev3.screen.print("Song:", selected_song_index)
        ev3.screen.print(songs[selected_song_index].name)
        if Button.CENTER in ev3.buttons.pressed():
            # send song and play song
            start_time = clock.time() + play_delay
            server.send_song(songs[selected_song_index], start_time) # tell client ev3 to play song at start time
            player.play(songs[selected_song_index], start_time) # play song on server ev3 at start time
            
            while Button.CENTER in ev3.buttons.pressed():
                pass

        if Button.LEFT in ev3.buttons.pressed():
            # previous song
            selected_song_index -= 1
            if selected_song_index < 0:
                selected_song_index = len(songs) - 1
            while Button.LEFT in ev3.buttons.pressed():
                pass
        if Button.RIGHT in ev3.buttons.pressed():
            # next song
            selected_song_index += 1
            if selected_song_index >= len(songs):
                selected_song_index = 0
            while Button.RIGHT in ev3.buttons.pressed():
                pass
        wait(50)
        ev3.screen.clear()



if __name__ == "__main__":
    main()