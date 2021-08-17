from logging import exception
from multiprocessing import queues
from multiprocessing.context import Process
from robot.RobotActions import NeuralNetWorkRead, RobotState
import RobotActions as RobotActions
import numpy as np
import cv2
from keras.preprocessing import image
import time
import os
import multiprocessing as mp
from enum import Enum
import RPi.GPIO as GPIO

GPIO_TRIGGER = 16
GPIO_ECHO = 20

def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00005)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if(StartTime-StopTime > 3):
            break
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if(StopTime - StartTime > 3):
            break        

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    GPIO.output(GPIO_TRIGGER, False)
    return distance

def RobotProccess(m):
    RobotController = RobotActions.RobotRunner(LogInfo = False)
    RobotController.RunState()
    while True :
        time.sleep(0.1)
        NNState = m['NeuralNetworkState']
        distance = m['distance']
        confidence = 1
        try :
            RobotController.Update(NNState,distance,confidence,None)
            RobotController.UpdateState()
            RobotController.RunState()
        except :
            print("Robot Error")

def DistanceProccess(m):
    while True:
        time.sleep(0.25)
        try:
            readDistance = distance()
            m['distance'] = readDistance
        except :
            print("Distance Error") 




def GetNeuralNetworkResponseProccess(m):
    start = time.time()

    while True:
        end = time.time()
        time.sleep(0.5)


if __name__ == '__main__':
    m = mp.Manager().dict()
    t = mp.Value('d',0)
    m['NeuralNetworkState'] = NeuralNetWorkRead.Stop
    m['distance'] = 0
    m['confidence'] = 1

    p1 = Process(target=RobotProccess,args=(m,))
    p2 = Process(target=DistanceProccess,args=(m,))
    p3 = Process(target=GetNeuralNetworkResponseProccess,args=(m,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
