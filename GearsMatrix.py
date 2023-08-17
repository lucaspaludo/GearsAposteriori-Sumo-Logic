#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from pybricks.parameters import *
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import *
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Create the sensors and motors objects

ev3 = EV3Brick()

motorEsquerdo = Motor(Port.A)
motorDireito = Motor(Port.B)

color_sensor_in1 = ColorSensor(Port.S1)
ultrasonic_sensor_in2 = UltrasonicSensor(Port.S2)
ultrasonic_sensor_in3 = UltrasonicSensor(Port.S3)
ultrasonic_sensor_in4 = UltrasonicSensor(Port.S4)


def matMult(matrix1, matrix2):
    result = [0, 0]

    for j in range(len(matrix2[0])):
        for k in range(len(matrix2)):
            result[j] += matrix1[k] * matrix2[k][j]
    
    return result

while True:
    
    #detecta a borda
    color = color_sensor_in1.color()
    if color <= 5:
        motorDireito.dc(-60)
        motorEsquerdo.dc(-60)
        wait(1300)
        
        motorEsquerdo.run_angle(-200, 400, then=Stop.HOLD, wait=False)
        motorDireito.run_angle(200, 400, then=Stop.HOLD, wait=True)
        
    # Leitura dos dados
    dist = [100.0/ultrasonic_sensor_in3.distance(),
            100.0/ultrasonic_sensor_in2.distance(),
            100.0/ultrasonic_sensor_in4.distance()]
    norm = sum(dist)
    dist = [x/norm for x in dist]
    
    m2 = [[100,-10],[50,50],[-10,100]]
    
    res = matMult(dist, m2)
    motorDireito.dc(res[0])
    motorEsquerdo.dc(res[1])