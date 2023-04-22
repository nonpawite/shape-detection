#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Computer Vision Project:
    Shape Detection : Video

Created on Sat Apr 22 2023

@author: Jiraorj Thanudchaipuen
"""

import cv2   as cv
import numpy as np

# Define the width and height of the frame
frameWidth  = 640
frameHeight = 480

# Access the default camera (camera 0)
cap = cv.VideoCapture("D:\\iCloudDrive\\Documents\\Adobe\\After Effect\\Object Moving_AME\\Comp 1.mp4")

# Set the frame height and width
cap.set(3, frameHeight)
cap.set(4, frameWidth)


# Empty Function
def empty(x):
    pass


# Detect Shape Function
def getShape(cnt):
    shape = "Unknown"
    
    # Find number of edges in poltgon   
    peri   = cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
    edges  = len(approx)
    
    if edges == 3:
        shape = "Triangle"
    elif edges == 4:
        # Check if shape is a square or a rectangle based on aspect ratio
        x, y, w, h  = cv.boundingRect(approx)
        aspectRatio = float(w)/h
        
        if aspectRatio >= 0.95 and aspectRatio <= 1.05:
            shape = "Square"
        else:
            shape = "Rectangle"
    elif edges == 5:
        shape  = "Pentagon"
    elif edges == 6:
        shape  = "Hexagon"
    else:
        shape = "Circle"
    return shape


cv.namedWindow("Shape Detection")

cv.createTrackbar("Threshold1", "Shape Detection", 100,  255,   empty)
cv.createTrackbar("Threshold2", "Shape Detection", 200,  255,   empty)
cv.createTrackbar("Area",       "Shape Detection", 2000, 20000, empty)


# Draw Contour Function
def getContours(imgDil, imgContour):
    # Find contours using RETR_EXTERNAL mode and CHAIN_APPROX_SIMPLE method
    contours, _ = cv.findContours(imgDil, 
                                  cv.RETR_EXTERNAL, 
                                  cv.CHAIN_APPROX_SIMPLE)

    # Loop through all the contours found in the image
    for cnt in contours:
        # Get minimum area from slider
        areaMin = cv.getTrackbarPos("Area", "Shape Detection")
        # Get the area of the contour
        area = cv.contourArea(cnt)

        if area > areaMin:
            # Draw contour
            cv.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)

            # Get shape
            shape = getShape(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            
            # Draw shapes and name
            cv.rectangle(imgContour, 
                         (x, y), (x + w, y + h), 
                         (0, 255, 0), 3)
            cv.putText(imgContour, shape, 
                       (x + w + 20, y + 45), 
                       cv.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 0, 255), 0)


# Main Loop
while cap.isOpened():
    # Capture frame
    _, img     = cap.read()
    img        = cv.resize(img, (890, 500))
    imgContour = img.copy()

    # Post Processing
    imgBlur = cv.GaussianBlur(img, (7, 7), 1)
    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)
    
    # Get threshold parameters
    t1 = cv.getTrackbarPos("Threshold1", "Shape Detection")
    t2 = cv.getTrackbarPos("Threshold2", "Shape Detection")

    imgCanny = cv.Canny(imgGray, t1, t2)
    
    # Dilating the binary edge-detected image 
    kernel = np.ones((5, 5))
    imgDil = cv.dilate(imgCanny, kernel, iterations = 1)
    getContours(imgDil, imgContour)
    
    # Output Result
    
    imgCanny = cv.cvtColor(imgCanny, cv.COLOR_GRAY2RGB)
    imgstack = np.vstack([img, imgCanny])
    cv.imshow("Shape Detection", imgstack)
    
    # Wait for use to press 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()