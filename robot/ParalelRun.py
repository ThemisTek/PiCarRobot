from multiprocessing import queues
from multiprocessing.context import Process
# from robot.RobotActions import RobotState
# import RobotActions as RobotActions
import numpy as np
import cv2
from keras.preprocessing import image
import time
import os
import multiprocessing as mp
from enum import Enum

class RobotState(Enum):
    Initial = 0
    MovingForward = 1
    TurningRight = 2
    TurningLeft = 3
    Stop = 4
    PreparedToTurnRight = 5
    PrepartedToTurnLeft = 6

class Test() : 
    def __init__(self):
        self.State = RobotState.Initial
        self.dif = 0


    def SetState(self,newState):
        self.State = newState    
    def print(self):
        print(self.State)
    def Start(self):
        self.p1.start()
        self.p2.start()
        self.p1.join()
        self.p2.join()

def GetTime(t,m):
    print("startGetTime")
    start = time.time()
    while True:
        end = time.time()
        time.sleep(0.5)
        t.value = end-start
        state = m['State']
        print(state)


def OutPutAction(t,m):
    print("StartOutPut")

    while True:
        time.sleep(0.05)
        if(t.value<1):
            m['State'] = RobotState.MovingForward
            print("Less 1")
        elif(t.value<3):
            m['State'] = RobotState.TurningRight
            print("Less 2")
        elif(t.value<10):
            m['State'] = RobotState.TurningLeft

if __name__ == '__main__':
    m = mp.Manager().dict()
    t = mp.Value('d',0)
    m['State'] = RobotState.Initial

    p1 = Process(target=GetTime,args=(t,m))
    p2 = Process(target=OutPutAction,args=(t,m))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
