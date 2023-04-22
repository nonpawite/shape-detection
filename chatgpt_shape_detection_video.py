import cv2 as cv
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv.VideoCapture(1)

cap.set(3, frameHeight)
cap.set(4, frameWidth)

def empty(x):
    pass

def getShape(cnt):
    shape = "Unknown"
    peri = cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
    edges = len(approx)

    if edges == 3:
        shape = "Triangle"
    elif edges == 4:
        x, y, w, h = cv.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio <= 1.05:
            shape = "Square"
        else:
            shape = "Rectangle"
    elif edges == 5:
        shape = "Pentagon"
    elif edges == 6:
        shape = "Hexagon"
    elif edges == 8:
        shape = "Octagon"
    elif edges == 10:
        shape = "Star"
    else:
        shape = "Circle"
    return shape

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)

cv.createTrackbar("Threshold1", "Parameters", 80, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 255, 255, empty)
cv.createTrackbar("Area", "Parameters", 2000, 20000, empty)

def getContours(imgDil, imgContour):
    contours, hierarchy = cv.findContours(imgDil, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        areaMin = cv.getTrackbarPos("Area", "Parameters")
        area = cv.contourArea(cnt)

        if area > areaMin:
            cv.drawContours(imgContour, cnt, -1, (255,0,0), 3)
            shape = getShape(cnt)
            x,y,w,h = cv.boundingRect(cnt)
            cv.rectangle(imgContour,(x,y),(x+w, y+h), (0,255,0), 3)
            cv.putText(imgContour, shape, (x+w+20,y+45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)

while cap.isOpened():
    ret, img = cap.read()
    imgContour = img.copy()

    imgBlur = cv.GaussianBlur(img, (7, 7), 1)

    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

    t1 = cv.getTrackbarPos("Threshold1", "Parameters")
    t2 = cv.getTrackbarPos("Threshold2", "Parameters")

    imgCanny = cv.Canny(imgGray, t1, t2)

    kernel = np.ones((5,5))
    imgDil = cv.dilate(imgCanny, kernel, iterations = 1)
    getContours(imgDil, imgContour=imgContour)

    imgGray = cv.cvtColor(imgGray, cv.COLOR_GRAY2BGR)
    imgCanny = cv.cvtColor(imgCanny, cv.COLOR_GRAY2BGR)
    imgDil = cv.cvtColor(imgDil, cv.COLOR_GRAY2BGR)

    imgstack = np.hstack([img, imgContour])

    cv.imshow('Output', imgstack)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
