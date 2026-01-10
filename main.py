#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


def run_motor(ev3):
    return_angle = 14

    motor = Motor(Port.A)

    motor.control.target_tolerances(speed=500, position=1) # change tollerance settings
    
    while True:
        motor.dc(100) #move motor at 100% speed
        if motor.angle() >= return_angle:
            motor.hold() # when target angle is reached, hold position
            break
    
    motor.run_target(-500, 0, then=Stop.HOLD, wait=True) # return to 0 position
    
    return
    

def reset_motor_angle():
    motor = Motor(Port.A)
    motor.run_until_stalled(-100, duty_limit=10) # Move motor until endstop
    motor.reset_angle(0) # Reset angle to zero
    print("Motor angle reset")
    return

def establish_connection_too_second_ev3(ev3):
    # Placeholder for establishing connection logic
    pass

def main():
    ev3 = EV3Brick()
    ev3.screen.set_font(Font(size=50, bold=True))

    clock = StopWatch() # create clock

    establish_connection_too_second_ev3(ev3)
    reset_motor_angle()


    while True:
        if Button.CENTER in ev3.buttons.pressed():
            run_motor(ev3)
        if Button.DOWN in ev3.buttons.pressed():
            break

        if clock.time()//200 % 10 == 0:
            #ev3.speaker.beep()  # Beep every 10 seconds
            ev3.light.on(Color.GREEN)
            run_motor(ev3)
        else:
            ev3.light.off()




if __name__ == "__main__":
    main()