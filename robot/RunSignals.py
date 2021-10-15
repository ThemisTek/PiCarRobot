from tensorflow.python.keras.layers.core import Dropout
import RobotActions as RobotActions
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.layers import Dense,Flatten,Dropout
from tensorflow.keras import Sequential
import cv2
import RPi.GPIO as GPIO
import time


GPIO_TRIGGER = 16
GPIO_ECHO = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

RobotController = RobotActions.RobotRunner(LogInfo = True)
RobotController.RunState()


def distance():
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00005)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
    # Περιμενουμε να γινει 1 και να πεσει στο 0
    # αν η διαρκεια περασει καποια δευτερολεπτα εχει γινει κατι λαθοσ και η διαδικασια σταματα
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if(StartTime-StopTime > 3):
            break
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if(StopTime - StartTime > 3):
            break       
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    GPIO.output(GPIO_TRIGGER, False)
    return distance


# Για να διαβαστουν τα βαρη τα εχουμε εξαγει και να ξαναφτιαξουμε το δικτυο
# το raspberry δεν μπορει να υποστηριξει τελευταιες εκδοσεις του keras
image_size = 96
mobile  = MobileNetV2(weights='imagenet',include_top=False,input_shape =(image_size,image_size,3),alpha = 0.35)
print(mobile.summary())
my_model = Sequential()
my_model.add(mobile)  
my_model.add(Dropout(0.5)) 
my_model.add(Flatten())
my_model.add(Dense(4, activation='softmax'))

allWeights = np.load('SignalsAllWeights.npy',allow_pickle=True)
i=0
for l in my_model.layers:
    weightsArray = []
    weights = l.get_weights()
    for subLayer in weights:
        weightsArray.append(allWeights[i])
        i+=1
    if(len(weightsArray)>0):
        l.set_weights(weightsArray)


IndexToState = {
     0 : RobotActions.NeuralNetWorkRead.Left,
     1 : RobotActions.NeuralNetWorkRead.Right,
     2 : RobotActions.NeuralNetWorkRead.Stop,
     3 : RobotActions.NeuralNetWorkRead.Up}

Labels = ['stop','right','left','up']          


cap = cv2.VideoCapture(0)
lastRead = time.time()

dist = distance()
resized_image = np.empty((image_size,image_size,3),np.uint8)
confidence = 0


while True:

    isTurning = RobotController.State == RobotActions.RobotState.TurningLeft or RobotController.State == RobotActions.RobotState.TurningRight 
    maxInd = 0

    bgr_image = cap.read()[1]
    resized_image = cv2.resize(bgr_image,(image_size,image_size))
    # Αν το ρομποτ στριβει τοτε δεν κανει υπολογισμο για να μην χαλασει το timing
    if(not isTurning):
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        proccesedImage = np.expand_dims(rgb_image,axis=0)
        proccesedImage = preprocess_input(proccesedImage)
        predictions = my_model.predict(proccesedImage)
        cv2.imshow("Threshold lower image", resized_image)
        l = cv2.waitKey(5) & 0XFF
        if(l == ord('q')):
            break
        maxInd = np.argmax(predictions)
        confidence = predictions[0][maxInd]

    now = time.time()    
    # Περνουμε δειγματα ανα 0.5 δευτερολεπτα για την αποσταση
    if(now - lastRead > 0.5):
        dist = distance()
        lastRead = time.time()

    NNState = IndexToState[maxInd]
    RobotController.Update(NNState,dist,confidence,resized_image)
    RobotController.UpdateState()
    RobotController.RunState()
 

