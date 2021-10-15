import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import cv2
from keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
import keras

image_size = 96
model = keras.models.load_model('signalsFull.h5')

train_datagen = ImageDataGenerator(
      rotation_range=5,
      width_shift_range=0.3,
      height_shift_range=0.3,
      zoom_range=0.2,
      brightness_range=(0.8,1.2),
      horizontal_flip=False,
      fill_mode='nearest')

# Ο DataGenerator διαβάζει τον φάκελο και από εκεί
# μπορούμε να αντιστοιχίσουμε την έξοδο του δικτύου
# με το όνομα του σήματος  

generator= train_datagen.flow_from_directory("./desktop/signals",target_size=  (image_size,image_size))
label_dict = (generator.class_indices)
print(label_dict)
label_map = {y:x for x,y in label_dict.items()}
print(label_map)

for _ in range(0):
    img,label = generator.next()
    print(type(img))
    predictions = model.predict(img[0:1,:,:,:])
    print(predictions[0] == label[0])
    imageThatGoesIn = img[0,:,:,:]
    cv2.imshow("",imageThatGoesIn)
    l = cv2.waitKey(0) & 0XFF
    if(l == ord('q')):
        break
    a = predictions[0][0]
    b = predictions[0][1]
    c = predictions[0][2]
    d = predictions[0][3]
    predString = f'{label_map[0]}:{a:0.2f} {label_map[1]}:{b:0.2f} {label_map[2]}:{c:0.2f} {label_map[3]}:{d:0.2f} label:{label[0]}'
    print(predString)

cap = cv2.VideoCapture(0)
while True:
    bgr_image = cap.read()[1]

    resized_image = cv2.resize(bgr_image,(image_size,image_size))
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    reshapedTestIm = np.expand_dims(rgb_image,axis=0)
    predictions = model.predict(reshapedTestIm)

    cv2.imshow("Threshold lower image", bgr_image)
    l = cv2.waitKey(5) & 0XFF
    if(l == ord('q')):
        break
    maxInd = np.argmax(predictions)
    a = predictions[0][0]
    b = predictions[0][1]
    c = predictions[0][2]
    d = predictions[0][3]
    predString = f'{label_map[0]}:{a:0.2f} {label_map[1]}:{b:0.2f} {label_map[2]}:{c:0.2f} {label_map[3]}:{d:0.2f}'
    print(predString)
