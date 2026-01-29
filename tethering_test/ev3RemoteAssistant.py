#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

import socket
import time
import os

#  -------------------------------------------------------------------------------------
# | This code is from this website: https://gitlab.com/LeeJenkins/RemoteEV3/-/tree/main |
#  -------------------------------------------------------------------------------------

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()
ev3.screen.set_font(Font(size=15, bold=True))


def getHostName():
    file = open('/etc/hostname','r')
    hostname = file.read()
    file.close()
    return hostname


def main():
    MAX_BUFFER_SIZE = 1024
    deviceMap           = { }
    remoteAssistantPort = 0xEB3
    socketAddr   = socket.getaddrinfo('0.0.0.0', remoteAssistantPort)[0][-1]
    serverSocket = socket.socket()
    serverSocket.bind(socketAddr)
    serverSocket.listen(1)

    ev3.screen.print('Remote Assistant')
    ev3.screen.print('host name',getHostName())
    ev3.screen.print('listen on port',remoteAssistantPort )
    print('Remote Assistant')
    print('host name',getHostName())
    print('listening on port',remoteAssistantPort,'at these addresses:' )
    os.system("ip address | grep 192.168 | sed 's/.*inet //g' | sed 's/\/.*//g'")

    RECV_BUFFER_SIZE = 1024
    while True:
        connection, address = serverSocket.accept()
        request = connection.recv(RECV_BUFFER_SIZE).decode("utf-8")
        response = dispatcher( deviceMap, request )
        connection.send(response)
        connection.close()
        # ev3.screen.print(time.time()-631152000)
        # ev3.screen.print(request)
        # ev3.screen.print(response)


def dispatcher( deviceMap, request ):
    status = "ERR"
    result = "Bad Request"
    routing,args = request.split(':')
    target,command = routing.split('.')
    argList = args.split(',')
    if target == 'remote' and command == 'name':
        status = "OK"
        result = getHostName()
    elif target == 'remote' and command == 'create':
        status,result = createDevice( deviceMap, argList )
    elif target in deviceMap:
        status,result = deviceMethod( deviceMap, target, command, argList )
    return status+":"+result


portArgMap = {
    'Port.A': Port.A,
    'Port.B': Port.B,
    'Port.C': Port.C,
    'Port.D': Port.D,
    'Port.S1': Port.S1,
    'Port.S2': Port.S2,
    'Port.S3': Port.S3,
    'Port.S4': Port.S4
}


def createDevice( deviceMap, argList ):
    global portArgMap
    status = "ERR"
    result = "Bad Request"

    if len(argList) == 2:
        target   = argList[0]
        portStr  = argList[1]
        # print("portStr is '"+portStr+"'")
        portArg  = portArgMap[ portStr ]
        instance = None
        try:
            if target == "TouchSensor":
                instance = TouchSensor( portArg )
            elif target == "InfraredSensor":
                instance = InfraredSensor( portArg )
            elif target == "UltrasonicSensor":
                instance = UltrasonicSensor( portArg )
            else:
                result = "unsupported object type "+target
        except:
            result = target + " not connected to "+portStr

        if instance:
            id = target + portStr.replace('.','')
            deviceMap[id] = instance
            status = "OK"
            result = id

    return status,result

def deviceMethod( deviceMap, target, command, argList ):
    status = "ERR"
    result = "cannot execute "+command+" of "+target
    try:
        instance = deviceMap[target]
        if command == 'pressed':
            result = str(instance.pressed())
            status = "OK"
        elif command == 'distance':
            result = str(instance.distance())
            status = "OK"
    except:
        pass # let's not crash here OK?
    return status, result


main()
