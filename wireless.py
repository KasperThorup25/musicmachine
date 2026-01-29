#!/usr/bin/env pybricks-micropython

from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox, NumericMailbox
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

import urandom
from random import randint

# this list contains the tasks that can be sent from main EV3 to second EV3
tasklist = {
    0: "SONG MODE",
    1: "TUNING MODE",
}


class Server:
    def __init__(self, ev3, clock):
        self.ev3 = ev3
        self.clock = clock
        self.server = self.establish_bluetooth_connection_SERVER(ev3) # connect to client

        self.sync_clocks_SERVER(clock, ev3) # sync clocks

    def establish_bluetooth_connection_SERVER(self, ev3):
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

    def sync_clocks_SERVER(self, clock, ev3):
        syncbox = NumericMailbox('synchronisation', self.server)
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
    
    def send_task(self, task):
        taskbox = NumericMailbox('task', self.server)
        print("sending task: ")
        taskbox.send(task)
        return

    def send_note(self, note):
        notebox = NumericMailbox('note', self.server)
        print("sending note: ", note)
        notebox.send(note)
        return

    def send_song (self, song, start_time):
        songbox = NumericMailbox('song', self.server)
        print("sending song: ", song.song_number)
        songbox.send(song.song_number)
        wait(200)
        print("sending start time: ", start_time)
        songbox.send(start_time)
        return


class Client:
    def __init__(self, ev3, clock):
        self.ev3 = ev3
        self.clock = clock
        self.client = self.establish_bluetooth_connection_CLIENT(ev3) # connect to server

        self.sync_clocks_CLIENT(self.client, clock, ev3) # sync clocks

    def establish_bluetooth_connection_CLIENT(self, ev3):
        SERVER_NAME = 'ev3dev'

        client = BluetoothMailboxClient()
        mbox = NumericMailbox('handshake', client)

        print('establishing connection...')
        client.connect(SERVER_NAME)
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

    def sync_clocks_CLIENT(self, client, clock, ev3):
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

    def wait_for_task(self):
        taskbox = NumericMailbox('task', self.client)
        print("waiting for task...")
        taskbox.wait()
        return int(taskbox.read())
    
    def wait_for_note(self):
        notebox = NumericMailbox('note', self.client)
        print("waiting for note...")
        notebox.wait()
        return int(notebox.read())

    def wait_for_song(self):
        songbox = NumericMailbox('song', self.client)
        print("waiting for song...")
        songbox.wait()
        song_number = int(songbox.read())
        print("waiting for start time...")
        songbox.wait()
        start_time = int(songbox.read())
        return song_number, start_time