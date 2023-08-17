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
color_sensor_in6 = ColorSensor(Port.S6)
ultrasonic_sensor_in2 = UltrasonicSensor(Port.S2)
ultrasonic_sensor_in8 = UltrasonicSensor(Port.S8)
ultrasonic_sensor_in7 = UltrasonicSensor(Port.S7)


def Desfuzzificar(low, mid, high):
    power = low*40 + mid*80 + high*120
    return (0 if (power == 120) else power)

# Here is where your code starts

'''
Range do sensor: 0 - 400cm;
Tamanho da arena: 160cm;

Fuzzificação:
Perto: 0 - 40cm;
Meio: 40 - 80cm;
Longe: 80 - 120cm;

Regras:
A detalhar.
'''

# Fuzzyficação dos dados
class FuzzyVariable:
    def __init__(self, name, low, mid, high):
        self.name = name
        self.low = low
        self.mid = mid
        self.high = high

    def low_membership(self, x):
        if x <= self.low:
            return 1
        elif x > self.low and x < self.mid:
            return (self.mid - x) / (self.mid - self.low)
        else:
            return 0

    def mid_membership(self, x):
        if x <= self.low or x >= self.high:
            return 0
        elif x > self.low and x <= self.mid:
            return (x - self.low) / (self.mid - self.low)
        elif x > self.mid and x < self.high:
            return (self.high - x) / (self.high - self.mid)
        else:
            return 0

    def high_membership(self, x):
        if x >= self.high:
            return 1
        elif x > self.mid and x < self.high:
            return (x - self.mid) / (self.high - self.mid)
        else:
            return 0
            
while True:
    
    #detecta a borda
    color_frente = color_sensor_in1.color()
    color_tras = color_sensor_in6.color()
    
    if color_frente == 5:
        motorDireito.dc(-60)
        motorEsquerdo.dc(-60)
        wait(2000)
        motorEsquerdo.dc(-100)
        motorDireito.dc(0)
        
    if color_tras == 5:
        motorDireito.dc(60)
        motorEsquerdo.dc(60)
        
    # Leitura dos dados
    distancia_sensor_1 = ultrasonic_sensor_in8.distance()/10
    distancia_sensor_2 = ultrasonic_sensor_in2.distance()/10
    distancia_sensor_3 = ultrasonic_sensor_in7.distance()/10
    #girarEsquerda(20)

    # Definição das variáveis linguísticas
    distancia = FuzzyVariable('Distância', 40, 80, 120)
    
    # Cálculo das funções de pertinência para o sensor 1
    fuzzy_low_1 =  [distancia.low_membership(distancia_sensor_1)]
    fuzzy_mid_1 =  [distancia.mid_membership(distancia_sensor_1)]
    fuzzy_high_1 = [distancia.high_membership(distancia_sensor_1)]
    
    # Cálculo das funções de pertinência para o sensor 2
    fuzzy_low_2 =  [distancia.low_membership(distancia_sensor_2)]
    fuzzy_mid_2 =  [distancia.mid_membership(distancia_sensor_2)]
    fuzzy_high_2 = [distancia.high_membership(distancia_sensor_2)]
    
    # Cálculo das funções de pertinência para o sensor 3
    fuzzy_low_3 =  [distancia.low_membership(distancia_sensor_3)]
    fuzzy_mid_3 =  [distancia.mid_membership(distancia_sensor_3)]
    fuzzy_high_3 = [distancia.high_membership(distancia_sensor_3)]
    
    # Apresentação dos dados
    #print(f'Rng | S1:{distancia_sensor_1:.2f} | S2:{distancia_sensor_2:.2f} | S3:{distancia_sensor_3:.2f}')
    #print(f'1 | Low:{fuzzy_low_1[0]:.3f} | Mid:{fuzzy_mid_1[0]:.3f} | High:{fuzzy_high_1[0]:.3f}')
    #print(f'2 | Low:{fuzzy_low_2[0]:.3f} | Mid:{fuzzy_mid_2[0]:.3f} | High:{fuzzy_high_2[0]:.3f}')
    #print(f'3 | Low:{fuzzy_low_3[0]:.3f} | Mid:{fuzzy_mid_3[0]:.3f} | High:{fuzzy_high_3[0]:.3f}')
    
    powers = [
    Desfuzzificar(fuzzy_low_1[0], fuzzy_mid_1[0], fuzzy_high_1[0]), 
    Desfuzzificar(fuzzy_low_2[0], fuzzy_mid_2[0], fuzzy_high_2[0]), 
    Desfuzzificar(fuzzy_low_3[0], fuzzy_mid_3[0], fuzzy_high_3[0])
    ]
    
    #print(f'Desfuzzi: {powers}')
    
    if powers[0] == 40 and powers[1] == 0 and powers[2] == 0:
        motorDireito.dc(100)
        motorEsquerdo.dc(0)
    
    if powers[0] == 40 and powers[1] == 40 and powers[2] == 0:
        motorDireito.dc(80)
        motorEsquerdo.dc(20)
        
    if powers[0] == 40 and (powers[1] != 40 and powers[1] != 0) and powers[2] == 0:
        motorDireito.dc(80)
        motorEsquerdo.dc(80)
    
    if powers[0] == 0 and powers[1] == 40 and powers[2] == 0:
        motorDireito.dc(100)
        motorEsquerdo.dc(100)
    
    if powers[0] == 0 and powers[1] == 40 and powers[2] == 40:
        motorDireito.dc(20)
        motorEsquerdo.dc(80)
        
    if powers[0] == 0 and powers[1] == 40 and (powers[2] != 40 and powers[2] != 0):
        motorDireito.dc(80)
        motorEsquerdo.dc(80)
        
    if powers[0] == 0 and powers[1] == 0 and powers[2] == 40:
        motorDireito.dc(0)
        motorEsquerdo.dc(100)
        
    if (powers[0] != 40 and powers[0] != 0) and powers[1] == 40 and powers[2] == 0:
        motorDireito.dc(80)
        motorEsquerdo.dc(80)
    
    if (powers[0] != 40 and powers[0] != 0) and powers[1] == 0 and powers[2] == 0:
        motorDireito.dc(70)
        motorEsquerdo.dc(30)
        
    if powers[0] == 0 and powers[1] == 0 and (powers[2] != 40 and powers[2] != 0) == 0:
        motorDireito.dc(30)
        motorEsquerdo.dc(70)
    
    if (powers[0] != 40 and powers[0] != 0) and (powers[1] != 40 and powers[1] != 0) and powers[2] == 0:
        motorDireito.dc(50)
        motorEsquerdo.dc(20)
        
    if powers[0] == 0 and (powers[1] != 40 and powers[1] != 0) and (powers[2] != 40 and powers[2] != 0):
        motorDireito.dc(20)
        motorEsquerdo.dc(50)
        
    if powers[0] == 0 and (powers[1] != 40 and powers[1] != 0) and powers[2] == 0:
        motorDireito.dc(80)
        motorEsquerdo.dc(80)
    
    if powers[0] == 0 and powers[1] == 0 and (powers[2] != 40 and powers[2] != 0):
        motorDireito.dc(30)
        motorEsquerdo.dc(70)
    
    if (powers[0] != 40 and powers[0] != 0) and (powers[1] != 40 and powers[1] != 0) and (powers[2] != 40 and powers[2] != 0):
        motorDireito.dc(80)
        motorEsquerdo.dc(80)
    
    
    
        
        
    
    
    
    
    
    
        
    
    
    
    
    
    
    
    