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
from tensorflow.keras.applications import MobileNetV2
# from tensorflow import keras
from tensorflow.keras.applications.mobilenet import preprocess_input
# from tensorflow.keras import layers
from tensorflow.keras.layers import Dense,Flatten,Input,Dropout
from tensorflow.keras import Sequential


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
    while (m['NetworkDone'] == 0):
        continue

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
    print('network starts')
    image_size = 100
    mobile  = MobileNetV2(weights='imagenet',include_top=False,input_shape =(image_size,image_size,3),alpha = 0.35)
    print(mobile.summary())
    my_model = Sequential()
    my_model.add(mobile)  
    my_model.add(Dropout(0.5)) 
    my_model.add(Flatten())
    my_model.add(Dense(4, activation='softmax'))

    allWeights = np.load('SignalsAllWeightsV2.npy',allow_pickle=True)
    i=0
    for l in my_model.layers:
        weightsArray = []
        weights = l.get_weights()
        for subLayer in weights:
            weightsArray.append(allWeights[i])
            i+=1
        if(len(weightsArray)>0):
            l.set_weights(weightsArray)


    IndexToState = {
        0 : RobotActions.NeuralNetWorkRead.Left,
        1 : RobotActions.NeuralNetWorkRead.Right,
        2 : RobotActions.NeuralNetWorkRead.Stop,
        3 : RobotActions.NeuralNetWorkRead.Up}

    Labels = ['stop','right','left','up']
    m['NetworkDone'] = 1
    print('network done')
    cap = cv2.VideoCapture(0)
    while True:
        time.sleep(0.5)
        bgr_image = cap.read()[1]

        resized_image = cv2.resize(bgr_image,(image_size,image_size))
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        proccesedImage = np.expand_dims(rgb_image,axis=0)
        # image_array = image.img_to_array(rgb_image)
        # img_array_expanded_dims = np.expand_dims(image_array, axis=0)
        proccesedImage = preprocess_input(proccesedImage)
        predictions = my_model.predict(proccesedImage)
        cv2.imshow("Threshold lower image", resized_image)
        l = cv2.waitKey(5) & 0XFF
        if(l == ord('q')):
            break
        maxInd = np.argmax(predictions)
        NNState = IndexToState[maxInd]
        m['NeuralNetworkState'] = NNState


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
    m['NetworkDone'] = 0
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
