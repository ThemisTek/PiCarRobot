

import numpy as np
from IPython.display import Image
import tensorflow as tf 
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications import MobileNetV2
import cv2
import queue
import threading
import keras

SaveList = []
model = keras.models.load_model('signalsFullV2.h5')

print(model.summary())

i = 0

for l in model.layers:
    print(l.name)
    if(l.name == 'tf.math.truediv' or l.name == 'tf.math.subtract' or l.name == 'image_input'):
        continue
    weights = l.get_weights()
    for subLayer in weights:
        SaveList.append(subLayer)
        i+=1

np.save('./robot/SignalsAllWeightsV2.npy',SaveList)
