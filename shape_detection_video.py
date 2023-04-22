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
cap = cv.VideoCapture(1)

# Set the frame height and width
cap.set(3, frameHeight)
cap.set(4, frameWidth)

# Define an empty function that does nothing
def empty(x):
    pass

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)

cv.createTrackbar("Threshold1", "Parameters", 100, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 200, 255, empty)
cv.createTrackbar("Area", "Parameters", 2000, 20000, empty)

def getContours(imgDil, imgContour):
    contours, hierarchy = cv.findContours(imgDil, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for cnt in contours:
        areaMin = cv.getTrackbarPos("Area", "Parameters")
        area = cv.contourArea(cnt)
        #print(area)

        if area > areaMin:
            #print(area)
            cv.drawContours(imgContour, cnt, -1, (255,0,0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            print(len(approx))
            x,y,w,h = cv.boundingRect(approx)
            cv.rectangle(imgContour,(x,y),(x+w, y+h), (0,255,0), 3)
            
            #cv.putText(imgContour, "Points: " +str(len(approx)),(x+w+20,y+20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 0)
            #cv.putText(imgContour, "Areas: " +str(int(area)),(x+w+20,y+45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)

            edges = len(approx)
            if(edges == 3):
                cv.putText(imgContour, "Triangle", (x+w+20,y+65), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)

            elif(edges == 4):
                cv.putText(imgContour, "Rectangles", (x+w+20,y+45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)

            elif(edges == 8):
                cv.putText(imgContour, "Polygons", (x+w+20,y+45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)

            else:
                cv.putText(imgContour, "Unknown", (x+w+20,y+45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)


# Create a window named "Parameters" and set its size
#cv.namedWindow("Parameters")
#cv.resizeWindow("Parameters", 640, 240)

# Create two trackbars to adjust the thresholds for Canny edge detection
#cv.createTrackbar("Threshold1", "Parameters", 100, 255, empty)
#cv.createTrackbar("Threshold2", "Parameters", 200, 255, empty)

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
    kernel = np.ones((5,5))
    imgDil = cv.dilate(imgCanny, kernel, iterations = 1)
    getContours(imgDil, imgContour=imgContour)

    imgGray = cv.cvtColor(imgGray, cv.COLOR_GRAY2BGR)
    imgCanny = cv.cvtColor(imgCanny, cv.COLOR_GRAY2BGR)
    imgDil = cv.cvtColor(imgDil, cv.COLOR_GRAY2BGR)

    # Combine the original image and the Canny image side-by-side for display purposes
    imgstack = np.hstack([img, imgContour])

    # Display the combined image
    #cv.imshow('Original Image', img)
    #cv.imshow('Blur Image', imgBlur)
    cv.imshow('Output', imgstack)

    # If the 'q' key is pressed, exit the loop and release the camera
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()