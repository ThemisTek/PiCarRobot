import keras
from keras import backend as K
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
from keras.layers import Input, Flatten, Dense
import numpy as np
from IPython.display import Image
from keras.optimizers import Adam
import tensorflow as tf 
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications import MobileNetV2

image_size = 64
mobile = mobile = MobileNetV2(weights='imagenet',include_top=False,input_shape=(image_size,image_size,3))
print(mobile.summary())

# for l in mobile.layers:
#     l.trainable = False

input = Input(shape=(image_size,image_size,3),name = 'image_input')
outPutMob = mobile(input)

x = Flatten(name='flatten')(outPutMob)
x = Dense(4, activation='softmax', name='predictions')(x)
my_model = tf.keras.Model(inputs = input, outputs=x)

train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=20,
      width_shift_range=0.4,
      height_shift_range=0.4,
      horizontal_flip=False,
      fill_mode='nearest')

validation_datagen = ImageDataGenerator(rescale=1./255, 
      rotation_range=20,
      width_shift_range=0.4,
      height_shift_range=0.4)

train_dir = "./desktop/signals"
validation_dir = "./desktop/signals_val"
train_batchsize = 30

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=train_batchsize,
        class_mode='categorical')

val_batchsize=15

validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(image_size, image_size),
        batch_size=val_batchsize,
        class_mode='categorical',
        shuffle=False)


fnames = validation_generator.filenames

label2index = validation_generator.class_indices

idx2label = dict((v,k) for k,v in label2index.items())

print(idx2label)


opt = keras.optimizers.RMSprop(lr=0.001)
my_model.compile(loss='categorical_crossentropy',
optimizer=opt,
metrics=['accuracy'])

history = my_model.fit_generator(
      train_generator,
      steps_per_epoch=train_generator.samples/train_generator.batch_size ,
      epochs=35,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples/validation_generator.batch_size ,
      verbose=1)


my_model.save('signalsFullV2.h5')
my_model.save_weights(filepath='signalsWeightsFullV2.h5')