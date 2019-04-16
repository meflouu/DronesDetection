import cv2
import numpy as np
from time import time

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('small.mp4')
cv2.namedWindow("Trackbars")

cv2.createTrackbar("Lower Hue", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Lower Sat", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower Val", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper Hue", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Upper Sat", "Trackbars", 145, 255, nothing)
cv2.createTrackbar("Upper Val", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Erode", "Trackbars", 3, 20, nothing)
#cv2.createTrackbar("distance", "Trackbars", 3, 20, nothing)

#kernel = np.ones((5,5),np.uint8)

t = time()
i = 0

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx=0.3, fy=0.3)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("Lower Hue", "Trackbars")
    l_s = cv2.getTrackbarPos("Lower Sat", "Trackbars")
    l_v = cv2.getTrackbarPos("Lower Val", "Trackbars")
    u_h = cv2.getTrackbarPos("Upper Hue", "Trackbars")
    u_s = cv2.getTrackbarPos("Upper Sat", "Trackbars")
    u_v = cv2.getTrackbarPos("Upper Val", "Trackbars")
    ero = cv2.getTrackbarPos("Erode", "Trackbars")

    lower_limit = np.array([l_h, l_s, l_v])
    upper_limit = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    # mask = cv2.erode(mask,kernel,iterations = 1)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(30)
    if key == 27:
        break

    # fps measurements
    if i%30 == 0:
        print ("30 frames {}, fps {:.2f}".format(i//30, i/(time() - t)))
    i += 1



print("lower HSV: {}, {}, {}".format(l_h, l_s, l_v) )
print("upper HSV: {}, {}, {}".format(u_h, u_s, u_v) )
print("erode:", ero)

cap.release()
cv2.destroyAllWindows()
