from logging import exception
from multiprocessing import queues
from multiprocessing.context import Process
from numpy.core.arrayprint import TimedeltaFormat
import RobotActions 
import numpy as np
import cv2
# from keras.preprocessing import image
import time
import os
import multiprocessing as mp
from enum import Enum
import RPi.GPIO as GPIO
from enum import Enum
import picar
from picar import front_wheels,back_wheels
import time
import logging
from vlogging import VisualRecord
from RobotActions import NeuralNetWorkRead

# class RobotState(Enum):
#     Initial = 0
#     MovingForward = 1
#     TurningRight = 2
#     TurningLeft = 3
#     Stop = 4
#     PreparedToTurnRight = 5
#     PrepartedToTurnLeft = 6
 
# class NeuralNetWorkRead(Enum):
#     Unknown = -1
#     Stop = 0
#     Right = 1
#     Left = 2
#     Up = 3

# class RobotRunner():
#     def __init__(self, TimeToSteer = 6, LogInfo = False,forwardSpeed = 40,turnSpeed = 35, confidenceNeeded = 0.90):
#         picar.setup()
#         self.bw = back_wheels.Back_Wheels()
#         self.fw = front_wheels.Front_Wheels()
#         self.PreviousState = RobotState.Initial
#         self.State = RobotState.Initial
#         self.NNState = NeuralNetWorkRead.Unknown
#         self.distance = 0
#         self.confidence = 0
#         self.confidenceNeeded = confidenceNeeded
#         self.lastTime = time.time()
#         self.curTime = time.time()
#         self.timeDif = 0
#         self.distanceToTurn = 35
#         self.TimeToSteer = TimeToSteer
#         self.FolderName = time.strftime("%Y%m%d-%H%M%S")
#         self.LogInfo = LogInfo
#         self.count = 0
#         self.forwardSpeed = forwardSpeed
#         self.turnSpeed = turnSpeed
#         if(LogInfo):
#             self.logger = logging.getLogger('./' + self.FolderName +'/logs.txt')
#             fh = logging.FileHandler(self.FolderName + '.html',mode = "w")
#             self.logger.setLevel(logging.INFO)
#             self.logger.addHandler(fh)
            

#     def Update(self,NNState,distance,confidence,imageRead = None):
#         self.count +=1
#         self.NNState = NNState
#         self.distance = distance
#         self.confidence = confidence
#         self.timeDif = self.curTime - self.lastTime
#         if(self.LogInfo and imageRead is not None and self.count % 1 == 0):
#             logText = f"Count :{self.count} State : {self.State} NN : {self.NNState} conf : {self.confidence:0.2f} dist : {self.distance:0.2f} timeElapsed : {self.timeDif:0.2f}"
#             self.logger.info(VisualRecord(logText,imageRead,str(self.count)))
    
#     def countTimeInState(self,changedState : bool):
#         self.curTime = time.time()
#         if(changedState):
#             self.lastTime = self.curTime
#         self.timeDif = self.lastTime - self.curTime

    
#     def PrintState(self):
#         print(f'State : {self.State} NN : {self.NNState} conf : {self.confidence:0.2f} dist : {self.distance:0.2f} timeElapsed : {self.timeDif:0.2f}')
    
#     def Conf(self):
#         return self.confidence >= self.confidenceNeeded

#     def UpdateState(self):
#         self.PrintState()
#         self.PreviousState = self.State
#         if(self.State == RobotState.Initial or self.State == RobotState.Stop):
#             if(self.NNState == NeuralNetWorkRead.Up and self.Conf()):
#                 self.State = RobotState.MovingForward
#                 print('changed to')
#                 self.PrintState()
#         elif(self.State == RobotState.MovingForward):
#             if(self.NNState == NeuralNetWorkRead.Stop and self.Conf() and self.distance < 30):
#                 self.State = RobotState.Stop
#                 print('changed to')
#                 self.PrintState()
#             elif(self.NNState == NeuralNetWorkRead.Right and self.Conf()):
#                 self.State = RobotState.PreparedToTurnRight
#                 print('changed to')
#                 self.PrintState()
#             elif(self.NNState == NeuralNetWorkRead.Left and self.Conf()):
#                 self.State = RobotState.PrepartedToTurnLeft
#                 print('changed to')
#                 self.PrintState()
#             elif(self.distance < 10):
#                 self.State = RobotState.Stop
#                 print('changed to')
#                 self.PrintState()
#         elif(self.State == RobotState.TurningRight or self.State == RobotState.TurningLeft):
#             if(self.timeDif > self.TimeToSteer):
#                 self.State = RobotState.MovingForward
#                 print('changed to')
#                 self.PrintState()
#         elif(self.State == RobotState.PrepartedToTurnLeft):
#             if(self.NNState == NeuralNetWorkRead.Right and self.Conf()) :
#                 self.State = RobotState.PreparedToTurnRight
#             elif(self.distance < self.distanceToTurn):
#                 self.State = RobotState.TurningLeft
#                 print('changed to')
#                 self.PrintState()
#         elif(self.State == RobotState.PreparedToTurnRight):
#             if(self.NNState == NeuralNetWorkRead.Left and self.Conf()) :
#                 self.State = RobotState.PreparedToTurnRight
#             elif(self.distance < self.distanceToTurn):
#                 self.State = RobotState.TurningRight
#                 print('changed to')
#                 self.PrintState()
#         self.countTimeInState(self.PreviousState != self.State)

#     def RunState (self):
#         if(self.State == RobotState.Initial or self.State == RobotState.Stop):
#             self.bw.speed = 0
#             self.fw.turn(90)
#             self.bw.stop()
#         elif(self.State == RobotState.MovingForward or self.State == RobotState.PreparedToTurnRight or self.State == RobotState.PrepartedToTurnLeft):
#             self.fw.turn(90)
#             self.bw.speed = self.forwardSpeed
#             self.bw.backward()
#         elif(self.State == RobotState.TurningLeft):
#             self.fw.turn(45)
#             self.bw.speed = self.turnSpeed
#             self.bw.backward()
#         elif(self.State == RobotState.TurningRight):
#             self.fw.turn(45 + 90)
#             self.bw.speed = self.turnSpeed
#             self.bw.backward()
        


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
    RobotController = RobotActions.RobotRunner(LogInfo = False,InitCar = False)
    RobotController.RunState()
    print("InitDone")
    m['Start'] = 1
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
    while(m['Start'] == 0):
        continue

    while True:
        time.sleep(0.25)
        try:
            readDistance = distance()
            m['distance'] = readDistance
        except :
            print("Distance Error") 

def GetStateByTime(timeDif):
    NNState = NeuralNetWorkRead.Stop
    if(timeDif <= 1):
        NNState = NeuralNetWorkRead.Stop
    elif(timeDif <=3):
        NNState = NeuralNetWorkRead.Left
    elif(timeDif<= 12):
        NNState = NeuralNetWorkRead.Up
    elif(timeDif<=20):
        NNState = NeuralNetWorkRead.Right
    else :
        NNState = NeuralNetWorkRead.Stop
    
    return NNState


def GetNeuralNetworkResponseProccess(m):

    while(m['Start'] == 0):
        continue
    start = time.time()
    while True:
        end = time.time()
        dif = end - start
        m['NeuralNetworkState'] = GetStateByTime(dif)
        time.sleep(0.5)


if __name__ == '__main__':
    print("starting")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
    GPIO.setup(GPIO_ECHO,GPIO.IN)

    m = mp.Manager().dict()
    t = mp.Value('d',0)
    m['NeuralNetworkState'] = NeuralNetWorkRead.Stop
    m['distance'] = 0
    m['confidence'] = 1
    m['Start'] = 0
    picar.setup()
    p1 = Process(target=RobotProccess,args=(m,))
    p2 = Process(target=DistanceProccess,args=(m,))
    p3 = Process(target=GetNeuralNetworkResponseProccess,args=(m,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
