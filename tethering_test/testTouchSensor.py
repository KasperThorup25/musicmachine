#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

from ev3RemoteCommander import RemoteCommander, RemoteTounchSensor, RemoteUltrasonicSensor

import socket
import sys
import time

#  -------------------------------------------------------------------------------------
# | This code is from this website: https://gitlab.com/LeeJenkins/RemoteEV3/-/tree/main |
#  -------------------------------------------------------------------------------------

# This file was used to experiment with threading between two EV3's. Which indeed was achieved but was not chosed for this project because of complexity
# Reminder: 
# - Cable needed: USB-A to MINI-USB
# - The EV3 running this program must have the cable plugged into the USB A port 

# This program requires LEGO EV3 MicroPython v2.0 or higher.

# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()
ev3.screen.set_font(Font(size=15, bold=True))


def connectToRemoteEV3():
    """
    it's easier to write and debug code with the EV3's on
    the WiFi. but communication is much faster over the
    tethered connection. this function will look for the
    remote assistant at one address, then the other.
    """
    addressList = [
        "192.168.1.122", # WiFi LAN address
        "192.168.0.1"    # USB tethered
    ]
    for addr in addressList:
        remoteEV3 = RemoteCommander(addr)
        if remoteEV3.isReady():
            break
        else:
            remoteEV3 = None

    if not remoteEV3:
        print("ERROR: cannot find remote assistant")
        ev3.screen.print("ERROR: cannot find\nremote assistant")
        time.sleep(99)
        sys.exit(1)

    return remoteEV3

def main():
    remoteEV3 = connectToRemoteEV3()
    remoteTounchSensorPort4 = RemoteTounchSensor( remoteEV3, "Port.S4" )
    for i in range(9999):
        if remoteTounchSensorPort4.pressed():
            ev3.light.on(Color.GREEN)
        else:
            ev3.light.off()

main()
