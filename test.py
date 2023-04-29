#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 18:54:57 2023

@author: jiraorjthanudchaipuen
"""

import cv2 as cv
import numpy as np

# Define the width and height of the frame
frameWidth = 640
frameHeight = 480

# Access the default camera (camera 0)
cap = cv.VideoCapture(0)

# Set the frame height and width
cap.set(3, frameHeight)
cap.set(4, frameWidth)

def my_function():
    # create a VideoCapture object to capture frames from the camera
    cap = cv.VideoCapture(0)
    
    # create a variable to control whether or not to capture frames
    capture_frames = False
    
    while True:
        # read a frame from the camera
        ret, frame = cap.read()
        
        # check if the capture_frames variable is True
        if capture_frames:
            # perform shape detection on the frame
            # ...
            # display the frame with shape detection
            cv.imshow('Video Shape Detection', frame)
        
        # wait for a key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    # release the camera and destroy all windows
    cap.release()
    cv.destroyAllWindows()

def getContours(imgDil, imgContour):
    # ...
    # your code for shape detection
    # ...

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)

cv.createTrackbar("Threshold1", "Parameters", 100, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 200, 255, empty)
cv.createTrackbar("Area", "Parameters", 2000, 20000, empty)

# While the camera is open, perform the following actions
while cap.isOpened():
    
    # Read the current frame from the camera
    ret, img = cap.read()
    imgContour = img.copy()

    # Apply a Gaussian blur to the image to remove noise
    imgBlur = cv.GaussianBlur(img, (7, 7), 1)

    # Convert the image to grayscale
    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

    # Get the current values of the trackbars
    t1 = cv.getTrackbarPos("Threshold1", "Parameters")
    t2 = cv.getTrackbarPos("Threshold2", "Parameters")

    # Print the current threshold values
    #print(t1, t2)

    # Apply Canny edge detection to the grayscale image using the current threshold values
    imgCanny = cv.Canny(imgGray, t1, t2)

    # Convert the grayscale and Canny images to color for display purposes
    kernel = np.ones((5, 5))
    imgDil = cv.dilate(imgCanny, kernel, iterations=1)
    imgContour = img.copy()
    getContours(imgDil, imgContour)

    # Show the current frame with shape detection
    cv.imshow('Frame', imgContour)

    # Exit if the user presses the 'q' key
    if cv.waitKey(1) == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv.destroyAllWindows()
