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


portlist = [Port.A, Port.B, Port.C, Port.D]


def run_motor(ev3, port):
    return_angle = 5

    try:
        motor = Motor(port)
        motor.control.target_tolerances(speed=500, position=1) # change tollerance settings
    
        while True:
            motor.dc(100) #move motor at 100% speed
            if motor.angle() >= return_angle:
                motor.hold() # when target angle is reached, hold position
                break
    
        motor.run_target(-500, 0, then=Stop.HOLD, wait=True) # return to 0 position
    except Exception as e:
        print("Error running motor at: {}".format(port), e)
    return

def run_motor2(ev3, motor):
    motor.dc(100) #move motor at 100% speed
    wait(40)
    motor.hold() # when target angle is reached, hold position
    motor.run_target(-500, 0, then=Stop.HOLD, wait=True) # return to 0 position

    return
    

def reset_motor_angle(port):
    try:
        motor = Motor(port)
        motor.run_until_stalled(-100, duty_limit=10) # Move motor until endstop
        motor.reset_angle(0) # Reset angle to zero
        print("Motor angle reset at: {}".format(port))
        return
    except Exception as e:
        print("Error resetting motor angle at: {}".format(port), e)
        return


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

def main():
    ev3 = EV3Brick()
    ev3.screen.set_font(Font(size=50, bold=True))

    clock = StopWatch() # create clock
    #server = establish_bluetooth_connection(ev3) # return server object from bluetooth connection
    #sync_clocks(server, clock, ev3) # sync clocks between server and client
    #reset_motor_angle()



    for port in portlist:
        # reset motor angle
        reset_motor_angle(port)

    for port in portlist:
        # activate motor
        m = Motor(port)
        m.control.target_tolerances(speed=500, position=1)
        run_motor2(ev3, m)
        pass

    motor1 = Motor(Port.A)
    motor1.control.target_tolerances(speed=500, position=1)
    m1 = threading.Thread(target=run_motor2, args=(ev3, motor1))

    motor2 = Motor(Port.B)
    motor2.control.target_tolerances(speed=500, position=1)
    m2 = threading.Thread(target=run_motor2, args=(ev3, motor2))

    motor3 = Motor(Port.C)
    motor3.control.target_tolerances(speed=500, position=1)
    m3 = threading.Thread(target=run_motor2, args=(ev3, motor3))

    motor4 = Motor(Port.D)
    motor4.control.target_tolerances(speed=500, position=1)
    m4 = threading.Thread(target=run_motor2, args=(ev3, motor4))

    motor_threading_list = [m1, m2, m3, m4]

    for t in motor_threading_list:
        t.start()
        wait(250)
    
    for t in motor_threading_list:
        t.start()
        wait(200)

    for t in motor_threading_list:
        t.start()
        wait(150)

    for t in motor_threading_list:
        t.start()
        wait(100)

    for t in motor_threading_list:
        t.start()
        wait(50)

    wait(1000)



def test():
    ev3 = EV3Brick()
    ev3.screen.set_font(Font(size=50, bold=True))

    clock = StopWatch() # create clock
    reset_motor_angle(Port.A)

    cycle_count = 5

    times = [0] * cycle_count

    motor = Motor(Port.A)
    print("Motor limits:", end=" ")
    print(motor.control.limits())

    print("Motor PID:", end=" ")
    print(motor.control.pid())

    print("Motor target tolerances:", end=" ")
    print(motor.control.target_tolerances())

    motor.control.target_tolerances(speed=500, position=1)
    #motor.control.limits(speed=1000, acceleration=1500)

    for i in range(cycle_count):
        time_before = clock.time()
        run_motor2(ev3, motor)
        time_after = clock.time()

        times[i] = time_after - time_before
        print("motor run time (ms):", times[i])

        wait(100)

    print("Average motor run time (ms):", sum(times)/cycle_count)





main()
#test()