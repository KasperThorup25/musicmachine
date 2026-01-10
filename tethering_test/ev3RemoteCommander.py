#!/usr/bin/env pybricks-micropython

import socket
import sys

# This program requires LEGO EV3 MicroPython v2.0 or higher.

class RemoteCommander:

    def __init__(self,remoteAddressString):
        remoteAssistantPort = 0xEB3
        self.addressString  = remoteAddressString
        self.addressData    = socket.getaddrinfo( self.addressString, remoteAssistantPort )[0][-1]

    def isReady(self):
        # print("send remote name request")
        response = self.sendRequest('remote.name:',99)
        # print(response)
        status,result = response.split(':')
        return ( status == "OK" )

    def sendRequest( self, request, timeout=999 ):
        requestSocket = socket.socket()
        requestSocket.settimeout( timeout/1000 )
        try:
            requestSocket.connect( self.addressData )
            requestSocket.send(request)
            RECV_BUFFER_SIZE = 1024
            response = requestSocket.recv(RECV_BUFFER_SIZE).decode("utf-8")
        except:
            response = "ERR:no connection"
        requestSocket.close()
        return response


class RemoteDevice:
    def __init__(self,remote,deviceType,port):
        self.remote = remote
        response = self.remote.sendRequest( "remote.create:"+deviceType+","+port )
        status,result = response.split(':')
        if not status == "OK":
            print("ERROR attempting to create remote "+deviceType+" on",remote.addressString,"port",port)
            sys.exit(1)
        self.objectID = result


class RemoteTounchSensor(RemoteDevice):
    def __init__(self,remote,port):
        super().__init__(remote,"TouchSensor",port)
    def pressed(self):
        response = self.remote.sendRequest( self.objectID+".pressed:")
        status,result = response.split(':')
        return ( status == "OK" ) and ( result == "True" )

class RemoteUltrasonicSensor(RemoteDevice):
    def __init__(self,remote,port):
        super().__init__(remote,"UltrasonicSensor",port)
    def distance(self):
        response = self.remote.sendRequest( self.objectID+".distance:")
        status,result = response.split(':')
        distance = 987654321.0
        if status == "OK":
            distance = float(result)
        return distance
