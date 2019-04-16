import cv2
import numpy as np

def nothing(x):
	pass

cv2.namedWindow("Trackbars")

cv2.createTrackbar("Lower Hue", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Lower Sat", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower Val", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper Hue", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Upper Sat", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper Val", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Erode", "Trackbars", 3, 20, nothing)


img = cv2.imread("test.png")
img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


ero = cv2.getTrackbarPos("Erode", "Trackbars")


while ero < 10:
	print (ero)
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
	result = cv2.bitwise_and(img, img, mask=mask)

	cv2.imshow("result", result)
	cv2.moveWindow("result", 0,420)
	cv2.imshow("mask", mask)
	cv2.waitKey(100)




cv2.destroyAllWindows()