import keras
from keras import backend as K
from keras.layers.core import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet import preprocess_input
from keras.layers import Input, Flatten, Dense
from keras.optimizers import Adam
import tensorflow as tf 
from tensorflow.keras.applications import MobileNetV2
from tensorflow.python.keras.layers.core import Dropout
import pandas as pd
import time


# Δημιουργία του mobilenet 
# Αρχικά βάζουμε ένα τμήμα προ επεξεργασίας
# Έπειτα το mobilenet με τα βάρη από το imagenet και με τιμή alpha την μικρότερη
# και μέγεθος εικόνας την μικρότερη

image_size = 96
mobile = mobile = MobileNetV2(weights='imagenet',include_top=False,input_shape=(image_size,image_size,3),alpha = 0.35)

input = Input(shape=(image_size,image_size,3),name = 'image_input')
PreProccess = preprocess_input(input)
outPutMob = mobile(PreProccess)

x = Dropout(0.5,name="dropout")(outPutMob)
x = Flatten(name='flatten')(x)
x = Dense(4, activation='softmax', name='predictions')(x)
my_model = tf.keras.Model(inputs = input, outputs=x)

print(my_model.summary())

# Βάζουμε ένα τμήμα dropout ώστε να μειώσουμε το overfitting
# Τέλος με το Flatten 


train_datagen = ImageDataGenerator(
      rotation_range=5,
      width_shift_range=0.1,
      height_shift_range=0.1,
      zoom_range=0.2,
      brightness_range=(0.8,1.2),
      horizontal_flip=False,
      fill_mode='nearest')

validation_datagen = ImageDataGenerator(rotation_range=5,
      width_shift_range=0.1,
      height_shift_range=0.1,
      zoom_range=0.2,
      brightness_range=(0.8,1.2),
      horizontal_flip=False,
      fill_mode='nearest')

train_dir = "./desktop/signals"
validation_dir = "./desktop/signals_val"
train_batchsize = 35

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=train_batchsize,
        class_mode='categorical')

val_batchsize=25

validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(image_size, image_size),
        batch_size=val_batchsize,
        class_mode='categorical',
        shuffle=False)

# Δημιουργούμε τα 2 dataset 
# ένα για την εκπαίδευση του δικτύου 
# και ένα για την πιστοποίηση του

fnames = validation_generator.filenames

label2index = validation_generator.class_indices
idx2label = dict((v,k) for k,v in label2index.items())
print(idx2label)

opt = keras.optimizers.Adam(learning_rate=0.0001)
my_model.compile(loss='categorical_crossentropy',
optimizer=opt,
metrics=['accuracy'])

history = my_model.fit_generator(
      train_generator,
      steps_per_epoch=train_generator.samples/train_generator.batch_size ,
      epochs=90,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples/validation_generator.batch_size ,
      verbose=1)

my_model.save('signalsFull.h5')
my_model.save_weights(filepath='signalsWeightsFull.h5')

hist_df = pd.DataFrame(history.history)
strTime = time.strftime("%Y%m%d-%H%M%S")
histFileName = strTime + '_history'
with open(histFileName,mode="w") as f:
      hist_df.to_json(f)