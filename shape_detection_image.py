import cv2 as cv

img = cv.imread("C:\\Users\\Pennywise\\Documents\\toey\\Proj Tester\\test_data\\shapes.png")

width, height = 1500, 1000
imgresize = cv.resize(img, (width,height))

gray_img = cv.cvtColor(imgresize, cv.COLOR_BGR2GRAY)

gray = gray_img

_, thresh_image = cv.threshold(gray, 220, 255, cv.THRESH_BINARY)

contours, hierarchy = cv.findContours(thresh_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

for i, contour in enumerate(contours):
    if i == 0:
        continue

    epsilon = 0.01*cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    cv.drawContours(gray, contour, 0, (0,0,0), 4)

    x,y,w,h = cv.boundingRect(approx)
    x_mid = int(x + w/3)
    y_mid = int(y + h/1.5)

    coords = (x_mid, y_mid)
    colour = (0,0,0)
    font = cv.FONT_HERSHEY_DUPLEX

    if len(approx) == 3:
        cv.putText(gray, "Triangle", coords, font, 1, colour, 1)
    elif len(approx) == 4:
        cv.putText(gray, "Quadilateral", coords, font, 1, colour, 1)
    elif len(approx) == 5:
        cv.putText(gray, "Pentagon", coords, font, 1, colour, 1)
    elif len(approx) == 6:
        cv.putText(gray, "Hexagon", coords, font, 1, colour, 1)
    elif len(approx) == 7:
        cv.putText(gray, "Heptagon", coords, font, 1, colour, 1)
    elif len(approx) == 8:
        cv.putText(gray, "Octagon", coords, font, 1, colour, 1)
    elif len(approx) == 9:
        cv.putText(gray, "Nonagon", coords, font, 1, colour, 1)
    else:
        cv.putText(gray, "Circle", coords, font, 1, colour, 1)

cv.imshow("Output", gray)
cv.waitKey(0)
     