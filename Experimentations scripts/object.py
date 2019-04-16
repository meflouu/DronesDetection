import cv2
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
    pass

cv2.namedWindow("Trackbars", cv2.WINDOW_OPENGL)
cv2.createTrackbar("Altitude", "Trackbars", 0, 10, nothing)

cap = cv2.VideoCapture(0)
kernel = np.ones((30,30),np.uint8)

lower_limit = np.array([35, 15, 0])
upper_limit = np.array([112, 255, 93])

# lower_limit = np.array([0, 0, 26])
# upper_limit = np.array([179, 230, 160])

# 61 2 97
# 156 155 177

# lower_limit = np.array([50, 77, 26])
# upper_limit = np.array([179, 210, 101])

width = int(cap.get(3))  # float
height = int(cap.get(4)) # float

altitude = 100

center = (width//4, height//4)        # 640, 360
print(center)

# style.use('fivethirtyeight')
# fig = plt.figure()

# ax1 = fig.add_subplot(1,1,1)
# ax1.plot(linewidth=.1)

# xs = []
# ys = []


# def animate(i):
#     ax1.clear()
#     ax1.plot(xs, ys)


while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 1)

    # outline and arrows
    cv2.line(frame, (0,180), (640,180), (255,255,255), 1)
    cv2.line(frame, (320,0), (320,360), (255,255,255), 1)
    cv2.arrowedLine(frame, center, (320+30, 180), (0,255,255), 2)
    cv2.arrowedLine(frame, center, (320, 180-30), (0,255,255), 2)

    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
      #find the biggest area
      c = max(contours, key = cv2.contourArea)
      x,y,w,h = cv2.boundingRect(c)

      # draw the book contour (in green)
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])

      # calculations
      dis_x = (cX-320)//(1000//altitude)
      dis_y = (180-cY)//(1000//altitude)

      dis_display = "x: " + str(dis_x) + "cm " + "| y: " +  str(dis_y) + "cm"

      # put text and highlight the center
      cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
      cv2.putText(frame, dis_display, (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
      cv2.arrowedLine(frame, (cX,cY), center, (0,0,255), 2)


      print(cX-320, 180-cY)

      # xs.append(float(cX))
      # ys.append(float(cY))

      # plt.axis([-640, 640, -360, 360])
      # plt.scatter(cX-640, 360-cY)
      # plt.pause(0.033)
      # plt.show()
      # ani1 = animation.FuncAnimation(fig, animate, interval=30)
      # plt.show()



    result = cv2.bitwise_and(frame, frame, mask=mask)

    # convert the grayscale image to binary image
    # print(len(result.shape))
    # gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(gray_image,127,255,0)
    # M = cv2.moments(thresh)

    # # # calculate x,y coordinate of center
    # if M["m00"] != 0:
    #   cX = int(M["m10"] / M["m00"])
    #   cY = int(M["m01"] / M["m00"])
    #   # put text and highlight the center
    #   cv2.circle(result, (cX, cY), 5, (255, 255, 255), -1)
    #   cv2.putText(result, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)



    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(30)
    if key == 27:
        break
    elif key == 100:	# letter 'd'
    	altitude = int(input("New altitude: "))

cap.release()
cv2.destroyAllWindows()
