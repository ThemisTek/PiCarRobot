import RobotActions as RobotActions
import numpy as np
from IPython.display import Image
import tensorflow as tf 
from tensorflow.keras.applications import MobileNetV2
from tensorflow import keras
from tensorflow.keras import layers
import cv2
import queue
import threading
from keras import models
from keras.preprocessing import image
import RPi.GPIO as GPIO
import time


GPIO_TRIGGER = 16
GPIO_ECHO = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

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



image_size = 64
mobile  = MobileNetV2(weights='imagenet',include_top=False,input_shape =(image_size,image_size,3))
print(mobile.summary())

my_model = tf.keras.Sequential()

#for l in mobile.layers:
    #l.trainable = False
 
my_model.add(mobile)   
my_model.add(layers.Flatten())
my_model.add(layers.Dense(4, activation='softmax'))

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


Labels = ['stop','right','left','up']          

cap = cv2.VideoCapture(0)
lastRead = time.time()

RobotController = RobotActions.RobotRunner()
#distCl = DistanceClass(GPIO_ECHO,GPIO_TRIGGER)
dist = distance()

while True:
    bgr_image = cap.read()[1]
    #dist = distCl.LastDist()

    resized_image = cv2.resize(bgr_image,(image_size,image_size))
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image_array = image.img_to_array(rgb_image)
    img_array_expanded_dims = np.expand_dims(image_array, axis=0)
    proccesedImage = keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)
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
    NNState = RobotActions.NeuralNetWorkRead.Unknown
    if(maxInd == 0):
        NNState = RobotActions.NeuralNetWorkRead.Stop
    elif(maxInd == 1):
        NNState = RobotActions.NeuralNetWorkRead.Right
    elif(maxInd == 2):
        NNState = RobotActions.NeuralNetWorkRead.Left
    elif(maxInd == 3):
        NNState = RobotActions.NeuralNetWorkRead.Up
    RobotController.Update(NNState,dist,predictions[0][maxInd])
    RobotController.UpdateState()
    RobotController.RunState()
    # print(dist,predictions[0][maxInd],Labels[maxInd])
 

