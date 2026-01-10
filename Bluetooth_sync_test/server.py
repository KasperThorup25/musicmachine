#!/usr/bin/env pybricks-micropython
# This file is for the EV3 that will act as the master in the Bluetooth sync test.

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


def establish_bluetooth_connection(ev3):
    # make handshake protocol here
    server = BluetoothMailboxServer()
    mbox = NumericMailbox('handshake', server)

    # The server must be started before the client!
    print('waiting for connection...')  
    server.wait_for_connection()
    print('connected!')
    wait(2000)


    random_number = randint(1, 100)

    mbox.send(random_number) # send random number to client
    print('random number sent, now waiting for response...')
    mbox.wait()
    print('response received!')
    recieved_number = mbox.read()
    
    if recieved_number == random_number + 1: # check if client added 1
        print("Handshake successfull!")
        for i in range(3):
            ev3.light.on(Color.ORANGE)
            wait(50)
            ev3.light.off()
            wait(50)
    else:
        print("Handshake failed.")
        for i in range(3):
            ev3.light.on(Color.RED)
            wait(50)
            ev3.light.off()
            wait(50)

    return server




def sync_clocks(server, clock, ev3):
    syncbox = NumericMailbox('synchronisation', server)
    wait(2000)

    sync_sycles = 10
    syncbox.send(sync_sycles)  # send number of sync cycles to client
    wait(2000)

    time_difference = [0] * sync_sycles

    for i in range(sync_sycles):  # sync clocks x times
        syncbox.send(clock.time())  # send current time to client
        print("clocktime sent")
        
        syncbox.wait()
        client_time = syncbox.read()  # read time sent back from client

        time_difference[i] = clock.time() - client_time

        ev3.light.on(Color.ORANGE)
        wait(100)
        ev3.light.off()
        wait(100)


    syncbox.wait()
    recieved_average = syncbox.read()  # read average time difference from client

    print("Recieved average difference (ms):", recieved_average)

    average_difference = sum(time_difference) / sync_sycles
    print("Average time difference (ms):", average_difference)

    #calculnating avg delay time for bluetooth communication
    calculated_time_difference = (average_difference + recieved_average) / 2
    print("Calculated time difference between EV3 hubs (ms):", calculated_time_difference)

    estimated_avg_bluetooth_delay = average_difference - calculated_time_difference
    print("Estimated average bluetooth delay (ms):", estimated_avg_bluetooth_delay)

    # adjusting clock based on calculated time difference + magic delay compensation when pausing and resuming clock
    print("adjusting clock...")
    clock.pause()
    wait(calculated_time_difference - 10)
    clock.resume()







def display_clock(clock, ev3):
    if clock.time() > 999999:
        clock.reset()

    ev3.screen.draw_text(20, 20, str(clock.time()//100),text_color=Color.BLACK, background_color=None)  # Display time in seconds without milliseconds
    wait(50)
    ev3.screen.clear()  # Clear screen for next update






def main():
    ev3 = EV3Brick()
    ev3.speaker.beep()
    ev3.screen.set_font(Font(size=50, bold=True))
    

    clock = StopWatch() # create clock
    server = establish_bluetooth_connection(ev3) # return server object from bluetooth connection
    
    sync_clocks(server, clock, ev3) # sync clocks between server and client

    while True:
        #display_clock(clock, ev3)

        if clock.time()//100 % 10 == 0:
            #ev3.speaker.beep()  # Beep every 10 seconds
            ev3.light.on(Color.GREEN)
        else:
            ev3.light.off()




main()