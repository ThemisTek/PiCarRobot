
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import cv2
from keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
import keras

image_size = 100
model = keras.models.load_model('signalsFullV2.h5')


train_datagen = ImageDataGenerator()

generator= train_datagen.flow_from_directory("./desktop/signals")
label_dict = (generator.class_indices)
print(label_dict)
label_map = {y:x for x,y in label_dict.items()}
print(label_map)


cap = cv2.VideoCapture(0)
while True:
    bgr_image = cap.read()[1]

    bgr_image = cap.read()[1]

    resized_image = cv2.resize(bgr_image,(image_size,image_size))
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image_array = image.img_to_array(rgb_image)
    img_array_expanded_dims = np.expand_dims(image_array, axis=0)
    proccesedImage = preprocess_input(img_array_expanded_dims)
    # proccesedImage = np.dot(img_array_expanded_dims,1/255)
    predictions = model.predict(proccesedImage)
    

    
    cv2.imshow("Threshold lower image", resized_image)
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
