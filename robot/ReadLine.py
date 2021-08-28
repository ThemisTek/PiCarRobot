import cv2
import numpy as np

cap = cv2.VideoCapture(0)

image_size = 120
red_thres = 40
bg_thres = 50

while True:
    bgr_image = cap.read()[1]
    resized_image = cv2.resize(bgr_image,(image_size,image_size))
    resized_image = cv2.GaussianBlur(resized_image, (5,5), 0)
    hsv = cv2.cvtColor(resized_image,cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    redMask = cv2.inRange(hsv, lower_red, upper_red)
    mask = np.bitwise_or(mask0,mask1)
    # mask0+mask1
    redFilteredImage = cv2.bitwise_and(resized_image[:,:,2],resized_image[:,:,2],mask=mask)

    l = cv2.waitKey(5) & 0XFF
    edges = cv2.Canny(redFilteredImage,50,150,apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,30)
    
    if(lines is not None):
        cv2.imshow('line',lines)
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(resized_image,(x1,y1),(x2,y2),(0,0,255),2)

    cv2.imshow('readImage',resized_image)
    cv2.imshow('test',redFilteredImage)

    if(l == ord('q')):
        break
