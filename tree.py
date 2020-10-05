#!/usr/bin/env micropython
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_2, INPUT_3
from time import sleep
import sys

forwardBias = -45
backwardBias = -43

arm = LargeMotor(OUTPUT_D)
tank = MoveTank(OUTPUT_C, OUTPUT_B)
steering_tank = MoveSteering(OUTPUT_C, OUTPUT_B)
gyro = GyroSensor(INPUT_2)
color = ColorSensor(INPUT_3)
color.mode='COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown') #To get the direct colour use: colors[color.value()]

def slowDown(leftSpeedSlowDown, rightSpeedSlowDown):
    unifiedSpeed = 50
    while leftSpeedSlowDown > 50:
        leftSpeedSlowDown = leftSpeedSlowDown - 10
        rightSpeedSlowDown = rightSpeedSlowDown - 10
        tank.on_for_seconds(leftSpeedSlowDown, rightSpeedSlowDown, 0.05, brake=False)
    while unifiedSpeed > 10:
        tank.on_for_seconds(unifiedSpeed, unifiedSpeed, 0.05, brake=False)
        unifiedSpeed = unifiedSpeed - 10
    
    tank.off(brake=True)

def speedUp(leftSpeedAcceleration, rightSpeedAcceleration):
     targetSpeed = 70
     while leftSpeedAcceleration < targetSpeed:
         leftSpeedAcceleration += 6.25
         rightSpeedAcceleration += 6.25
         tank.on_for_seconds(leftSpeedAcceleration, rightSpeedAcceleration, 0.05, brake=False)


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

def tree():

    gyroReset()

    leftSpeed = 70
    rightSpeed = 70

    leftSpeedAcceleration = 25
    rightSpeedAcceleration = 25

    arm.on_for_rotations(SpeedPercent(-100), 25)

    steering_tank.on_for_degrees(-100, SpeedPercent(100), 100 , brake=True)

    gyroCalibrate()


    speedUp(leftSpeedAcceleration, rightSpeedAcceleration)
    tank.on_for_seconds(leftSpeed, rightSpeed, 0.825, brake=False)
    
    slowDown(leftSpeed, rightSpeed)
    gyroCalibrate()

    arm.on_for_seconds(SpeedPercent(15), 1)
    
    sleep(1)
    
    tank.on_for_seconds(-100, -100, 0.775, brake=True, block=True)
    arm.on_for_rotations(SpeedPercent(-100), 150)

    steering_tank.on_for_degrees(100, SpeedPercent(25), 120 , brake=True)

    tank.on(-100, -100)



    sleep(10)
    

tree()
