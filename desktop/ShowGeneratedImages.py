from keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
from tensorflow.python.ops.gen_array_ops import empty

image_size = 100

train_datagen = ImageDataGenerator(
      rotation_range=5,
      width_shift_range=0.3,
      height_shift_range=0.3,
      zoom_range=0.2,
      brightness_range=(0.8,1.2),
      horizontal_flip=False,
      fill_mode='nearest')

train_dir = "./desktop/signals"
train_batchsize = 5

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=train_batchsize,
        class_mode='categorical')

print(len(train_generator))

img,label = train_generator.next()
numpyImage = np.array(np.dot(img,255),np.uint8)
rowImage = np.empty((image_size,image_size,3))\

for v in range (5):
      image = train_generator.next()
      images = image[0]
      for i,imageVariation in enumerate(images):
            imageVariation = np.uint8(imageVariation)
            rgbImage = cv2.cvtColor(imageVariation,cv2.COLOR_BGR2RGB)
            if(i == 0):
                  rowImage = rgbImage
            else:
                  rowImage = np.concatenate((rowImage,rgbImage),axis=1)
      if(v == 0):
            fullImage = rowImage
      else :
            fullImage = np.concatenate((fullImage,rowImage),axis=0)

cv2.imshow('Generated Image',fullImage)
cv2.waitKey(0)
