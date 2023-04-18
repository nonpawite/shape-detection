#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Computer Vision Project:
    Canny Edge Calibration

Created on Sat Apr 15 2023

@author: Jiraorj Thanudchaipuen
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

# Define an empty function that does nothing
def empty(x):
    pass

# Create a window named "Parameters" and set its size
cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)

# Create two trackbars to adjust the thresholds for Canny edge detection
cv.createTrackbar("Threshold1", "Parameters", 100, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 200, 255, empty)

# While the camera is open, perform the following actions
while cap.isOpened():
    # Read the current frame from the camera
    ret, img = cap.read()

    # Apply a Gaussian blur to the image to remove noise
    imgBlur = cv.GaussianBlur(img, (7, 7), 1)

    # Convert the image to grayscale
    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

    # Get the current values of the trackbars
    t1 = cv.getTrackbarPos("Threshold1", "Parameters")
    t2 = cv.getTrackbarPos("Threshold2", "Parameters")

    # Print the current threshold values
    print(t1, t2)

    # Apply Canny edge detection to the grayscale image using the current threshold values
    imgCanny = cv.Canny(imgGray, t1, t2)

    # Convert the grayscale and Canny images to color for display purposes
    imgGray = cv.cvtColor(imgGray, cv.COLOR_GRAY2BGR)
    imgCanny = cv.cvtColor(imgCanny, cv.COLOR_GRAY2BGR)

    # Combine the original image and the Canny image side-by-side for display purposes
    imgstack = np.hstack([img, imgCanny])

    # Display the combined image
    cv.imshow('Output', imgstack)

    # If the 'q' key is pressed, exit the loop and release the camera
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
