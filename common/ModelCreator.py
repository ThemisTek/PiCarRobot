
from enum import Enum
from keras import preprocessing
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.layers.experimental.preprocessing import *

class NetworkEnum(Enum):
    MobileNetSimple = 0
    MobilenetExtra = 1
    TestPreprocess = 2

class NetworkModel:
    def __init__(self,networkType : NetworkEnum):
        self.networkType = networkType
    def GetNetwork(self):
        if(self.networkType == NetworkEnum.MobileNetSimple):
            image_size = 100
            alpha = 0.5
            mobile  = MobileNetV2(weights='imagenet',include_top=False,input_shape =(image_size,image_size,3),alpha = alpha)
            model = Sequential()
            model.add(mobile)  
            model.add(Flatten())
            model.add(Dense(4, activation='softmax'))
            return model
        if(self.networkType == NetworkEnum.TestPreprocess):
            image_size = 100
            alpha = 0.5
            mobile  = MobileNetV2(weights='imagenet',include_top=False,input_shape =(image_size,image_size,3),alpha = alpha)
            resize_layer = Sequential(
                [
                    preprocess_input()

                ])
            data_augmentation = Sequential([
                RandomZoom(0.1,0.2)
            ])
            model = Sequential([
                input,
                resize_layer,
                data_augmentation,
                mobile,
                Flatten(),
                Dense(4, activation='softmax')
            ])
            return model


    def GetName(self):
        self.name = 'network_'+str(self.networkType)

    