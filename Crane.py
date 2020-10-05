#!/usr/bin/env micropython

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_C, OUTPUT_B, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_2, INPUT_3 
import sys
import time
from time import sleep


arm = LargeMotor(OUTPUT_D)
tank = MoveTank(OUTPUT_C, OUTPUT_B)
steering_tank = MoveSteering(OUTPUT_C, OUTPUT_B)
gyro = GyroSensor(INPUT_2)

def gyroCalibrate():

    if gyro.angle > backwardBias and gyro.angle < forwardBias:
        print("Seems to be there")
    elif gyro.angle < backwardBias:
        while gyro.angle < backwardBias:
            steering_tank.on_for_degrees(100, SpeedPercent(100), 1)
    elif gyro.angle > forwardBias:
        while gyro.angle > forwardBias:
            steering_tank.on_for_degrees(-100, SpeedPercent(100), 1)
    
    tank.off(brake=True)

def gyroReset():
    #yep, this is how we have to reset the gyro angle to 0
    gyro.mode = 'GYRO-RATE'
    gyro.mode = 'GYRO-ANG'

forwardBias = -91
backwardBias = -89

gyroReset()
tank.on_for_seconds(50, 50, 0.6, brake = True)
sleep(0.25)
steering_tank.on_for_degrees(-75, SpeedPercent(75), 200, brake = True)
gyroCalibrate()
sleep(0.25)
tank.on_for_seconds(50, 50, 1.5, brake = True)
arm.on_for_rotations(SpeedPercent(75), -15, brake=True)
arm.on_for_rotations(SpeedPercent(-50), -0.0225, brake=False)