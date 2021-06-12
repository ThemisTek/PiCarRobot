import keras
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
import cv2
import numpy as np

image_size = 100

train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=5,
      width_shift_range=0.3,
      height_shift_range=0.3,
      zoom_range=0.2,
      brightness_range=(0.8,1.2),
      horizontal_flip=False,
      fill_mode='nearest')

train_dir = "./desktop/signals"
validation_dir = "./desktop/signals_val"
train_batchsize = 10

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=train_batchsize,
        class_mode='categorical')
for _ in range(5):
    img,label = train_generator.next()
    numpyImage = np.array(np.dot(img,255),np.uint8)

    cv2.imshow('yo',numpyImage[0])
    cv2.waitKey(0)