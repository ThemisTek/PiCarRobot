from tensorflow.python.keras.layers.core import Dropout
import RobotActions as RobotActions
import numpy as np
# from IPython.display import Image
from tensorflow.keras.applications import MobileNetV2
# from tensorflow import keras
from tensorflow.keras.applications.mobilenet import preprocess_input
# from tensorflow.keras import layers
from tensorflow.keras.layers import Dense,Flatten,Input,Dropout
from tensorflow.keras import Sequential
import cv2
from keras.preprocessing import image
import RPi.GPIO as GPIO
import time
import os


GPIO_TRIGGER = 16
GPIO_ECHO = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

RobotController = RobotActions.RobotRunner(LogInfo = True)
RobotController.RunState()

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
        
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    GPIO.output(GPIO_TRIGGER, False)
    return distance



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


cap = cv2.VideoCapture(0)
lastRead = time.time()

dist = distance()

while True:
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
    now = time.time()
    if(now - lastRead > 1):
        dist = distance()
        lastRead = time.time()
    NNState = IndexToState[maxInd]
    RobotController.Update(NNState,dist,predictions[0][maxInd],resized_image)
    RobotController.UpdateState()
    RobotController.RunState()
 

