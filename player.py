#!/usr/bin/env pybricks-micropython

import threading
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait


# The Player class is used by multiple different files to play the songs written in songs.py
class Player:
    def __init__(self, ev3, clock, local_notes, portlist):
        self.ev3 = ev3
        self.clock = clock
        self.local_notes = local_notes
        self.portlist = portlist
        self.motor_threading_list = [0] * 4  # Placeholder for motor threadings

        self.reset_motor_angles()  # reset motor angles on init
        self.create_threadings(portlist) # create motor threadings

    def play(self, song, start_time_ms):
        for event in song.events:
            target = start_time_ms + event["time_ms"]

            while self.clock.time() < target:
                pass

            for note in event["notes"]:
                if note in self.local_notes:
                    self.motor_threading_list[self.local_notes(note)].start() # play note in separate thread
                    print("Playing note:", note)
    
    def play_note(self, note):
        if note in self.local_notes:
            self.motor_threading_list[self.local_notes.index(note)].start() # play note in separate thread
            print("Playing note:", note)
        else:
            print("Note not in local notes")
        return

    # This is the fundamental function that runs 1 motor each time its called
    def run_motor(self, ev3, motor):
        motor.dc(100) #move motor at 100% speed
        wait(40)
        motor.hold() # hold position after 40 ms
        motor.run_target(-500, 0, then=Stop.HOLD, wait=True) # return to 0 position
        return

    # funciton to reset all the connected motor angles on the EV3
    def reset_motor_angles(self):
        for port in self.portlist:
            try:
                motor = Motor(port)
                motor.run_until_stalled(-100, duty_limit=10) # Move motor until endstop
                motor.reset_angle(0) # Reset angle to zero
                print("Motor angle reset at: {}".format(port))
                pass
            except Exception as e:
                print("Error resetting motor angle at: {}".format(port), e) # print error message if motor not connected
                pass
        print("All motor angles reset.")
        return

    # This function creates a separate thread for each motor
    def create_threadings(self, portlist):
        for port in portlist:
            m = Motor(port)
            m.control.target_tolerances(speed=500, position=1) # This line is very important for the run_motor function to work properly
            self.motor_threading_list[portlist.index(port)] = threading.Thread(target=self.run_motor, args=(self.ev3, m))
        print("Motor threadings created.")
        return
