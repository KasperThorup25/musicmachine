#!/usr/bin/env pybricks-micropython
# This file is for the EV3 that will act as the slave in the Bluetooth sync test.

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

# This file was used when testing the bluetooth connection between two EV3 hubs
# The EV3 running this program must be turned on AFTER the server EV3




def establish_bluetooth_connection(ev3):
    # This is the name of the remote EV3 or PC we are connecting to.
    SERVER = 'ev3dev'

    client = BluetoothMailboxClient()
    mbox = NumericMailbox('handshake', client)

    print('establishing connection...')
    client.connect(SERVER)
    print('connected!')
    
    wait(1000)

    mbox.wait()
    recieved_number = mbox.read()
    print("Received number:", recieved_number)

    for i in range(3):
        ev3.light.on(Color.ORANGE)
        wait(50)
        ev3.light.off()
        wait(50)

    recieved_number += 1  # add 1 to recieved number

    mbox.send(recieved_number)  # send back modified number

    return client


def sync_clocks(client, clock, ev3):
    syncbox = NumericMailbox('synchronisation', client)
    wait(100)

    syncbox.wait()
    sync_sycles = int(syncbox.read()) # get number of sync cycles
    print("Number of sync cycles:", sync_sycles)
    wait(100)

    time_difference = [0] * sync_sycles

    recieved_times = [0] * sync_sycles

    for i in range(sync_sycles):  # sync clocks x times
        print("waiting...")
        syncbox.wait()
        recieved_times[i] = syncbox.read()  # read time sent back from server

        time_difference[i] = recieved_times[i] - clock.time()
        print("recieved")

        ev3.light.on(Color.ORANGE)
        wait(100)
        ev3.light.off()
        wait(100)

        syncbox.send(clock.time())  # send current time to server

    average_difference = sum(time_difference) / sync_sycles
    print("Average time difference (ms):", average_difference)

    wait(500)
    syncbox.send(average_difference)  # send average difference to server


    '''
    for i in range(sync_sycles):
        syncbox.send(recieved_times[i])  # send
        print("Recieved time", i, ":", recieved_times[i])'''



def setup_local_clock():
    clock = StopWatch()
    return clock




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
    
    clock = setup_local_clock()

    client = establish_bluetooth_connection(ev3)
    
    sync_clocks(client, clock, ev3)

    while True:
        display_clock(clock, ev3)

        if clock.time()//100 % 10 == 0:
            #ev3.speaker.beep()  # Beep every 10 seconds
            ev3.light.on(Color.GREEN)
        else:
            ev3.light.off()




main()





