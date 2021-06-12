from tensorflow.python.keras.layers.core import Dropout
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
import time
import os

image_size = 100
mobile  = MobileNetV2(weights='imagenet',include_top=False,input_shape =(image_size,image_size,3),alpha = 0.35)
print(mobile.summary())
my_model = Sequential()
input = Input(shape=(image_size,image_size,3),name = 'image_input')
my_model.add(mobile)  
my_model.add(Dropout(0.5)) 
my_model.add(Flatten())
my_model.add(Dense(4, activation='softmax'))

allWeights = np.load('./robot/SignalsAllWeightsV2.npy',allow_pickle=True)
i=0
for l in my_model.layers:
    print(l.name)
    weightsArray = []
    weights = l.get_weights()
    for subLayer in weights:
        weightsArray.append(allWeights[i])
        i+=1
    if(len(weightsArray)>0):
        l.set_weights(weightsArray)
