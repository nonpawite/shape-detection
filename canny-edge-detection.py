#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Computer Vision Project:
    Canny Edge Detection

Created on Sat Apr 15 2023

@author: Jiraorj Thanudchaipuen
"""

import cv2
import numpy as np

frameWidth  = 640
frameHeight = 480

cap         = cv2.VideoCapture(0)

cap.set(3, frameHeight)
cap.set(4, frameWidth)

def empty(x):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)

cv2.createTrackbar("Threshold1", "Parameters", 100, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 200, 255, empty)

while cap.isOpened():
    ret,img  = cap.read()
    
    imgBlur  = cv2.GaussianBlur(img, (7,7), 1)
    imgGray  = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    
    t1       = cv2.getTrackbarPos("Threshold1", "Parameters")
    t2       = cv2.getTrackbarPos("Threshold2", "Parameters")
    
    print(t1, t2)
    imgCanny = cv2.Canny(imgGray,t1,t2)
    
    imgGray  = cv2.cvtColor(imgGray, cv2.COLOR_GRAY2BGR)
    imgCanny = cv2.cvtColor(imgCanny, cv2.COLOR_GRAY2BGR)
    imgstack = np.hstack([img,imgCanny])
    
    cv2.imshow('Output', imgstack)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()