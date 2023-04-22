import cv2
import numpy as np

# Load image and convert to grayscale
img = cv2.imread('/Users/jiraorjthanudchaipuen/Documents/GitHub/shape-detection/test_data/shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 100, 200)

# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Identify shapes using contour approximation
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    area = cv2.contourArea(cnt)

    if len(approx) == 3:
        shape_name = "Triangle"
    elif len(approx) == 4:
        if abs(approx[0][0][0] - approx[1][0][0]) == abs(approx[0][0][1] - approx[1][0][1]):
            shape_name = "Square"
        else:
            shape_name = "Rectangle"
    elif len(approx) == 5:
        shape_name = "Pentagon"
    elif len(approx) == 6:
        shape_name = "Hexagon"
    elif len(approx) == 7:
        shape_name = "Heptagon"
    elif len(approx) == 8:
        shape_name = "Octagon"
    elif len(approx) == 9:
        shape_name = "Nonagon"
    elif len(approx) == 10:
        shape_name = "Decagon"
    else:
        shape_name = "Circle"

    # Draw shape name on image
    cv2.putText(img, shape_name, (cnt[0][0][0], cnt[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# Show the result
cv2.imshow('Shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
