import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
from time import time
import random

def outline(w, h, center, frame):
	cv2.line(frame, (0, h//2), (w, h//2), (255,255,255), 1)					# horizontal x axis
	cv2.line(frame, (w//2, 0), (w//2, h), (255,255,255), 1)					# vertical y axis
	cv2.arrowedLine(frame, center, (w//2+30, h//2), (0,255,255), 1)
	cv2.arrowedLine(frame, center, (w//2, h//2-30), (0,255,255), 1)


def distance(x, y, altitude):
	relative_x = altitude * x / 1000
	relative_y = altitude * y / 1000
	dis_display = "x: {:.1f}cm, y: {:.1f}cm".format(relative_x, relative_y)
	return dis_display


def vector(w, h, x, y, df = 0.3, altitude=1):
	return (w//2 + int(x*df),  h//2 - int(y*df))


def main():
	style.use('seaborn')
	cap = cv2.VideoCapture('small_third.mp4')

	# kernel = np.ones((1,1),np.uint8)
	lower_limit = np.array([0, 0, 0])
	upper_limit = np.array([179, 145, 255])

	w = int(cap.get(3))  						# width: 	640    	(/2 = 320)
	h = int(cap.get(4)) 						# height: 360			(/2 = 180)
	center = (w//2, h//2) 					# (320, 180)

	# altitude
	# 320 1220 2300 2550
	#
	altitude = 220
	# from 220cm to 5000cm    in 530 frames

	# plot starting point but this is not the right way
	x = [113, 113]
	y = [-175, -175]
	z = [altitude, altitude]

	# interval
	interval = 750

	# plot figure
	fig2 = plt.figure()
	fig = plt.figure()

	# fig3d
	ax = Axes3D(fig)
	ax.set_xlim3d(-interval, interval)
	ax.set_ylim3d(-interval, interval)
	ax.set_zlim3d(0, altitude*2)
	line,  = ax.plot(x,y,z, linewidth=1)

	# fig2d
	ax2 = fig2.add_subplot(1,1,1)
	ax2.set_xlim(-interval, interval)
	ax2.set_ylim(-interval, interval)
	line2, = ax2.plot(x,y, linewidth=1)


	# window position and size
	fig.canvas.manager.window.wm_geometry("+%d+%d" % (w, h+40))
	fig.set_size_inches(6.4, 3.4, forward=True)
	fig2.canvas.manager.window.wm_geometry("+%d+%d" % (0, 2*h+40))
	fig2.set_size_inches(5, 2.8, forward=True)

	plt.show(block=False)

	# pre alloacted lists
	# x = [None] * int(5000)
	# y = [None] * int(5000)
	# z = [None] * int(5000)

	t = time()
	i = 0						# for fps
	n = 0 					# for plotting with preallocation
	frames = ""
	cX = 1
	cY = 1

	while True:
		altitude = altitude + random.uniform(-.35, .35)
		if i > 320 and i < 1220 and altitude < 5000:
			altitude += 5.2 + random.uniform(0.6, 0.1612)
		elif i >= 2300 and i <= 2550 and altitude > 180:
			altitude -= 11.5 + random.uniform(0.01, 1)

		_, frame = cap.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# mask
		mask = cv2.inRange(hsv, lower_limit, upper_limit)
		# mask = cv2.dilate(mask,kernel,iterations = 1)

		# result
		result = cv2.bitwise_and(frame, frame, mask=mask)


		_, thresh = cv2.threshold(mask, 40, 255, 0)
		_, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		if len(contours) != 0:
			outline(w, h, center, frame)
			# outline(w, h, center, result)

			# biggest contour
			c = max(contours, key = cv2.contourArea)
			xc,yc,wc,hc = cv2.boundingRect(c)
			cv2.rectangle(frame,(xc,yc),(xc+wc,yc+hc), (250,206,135), 1)


			# find centroid
			M = cv2.moments(c)
			if M["m00"] != 0:
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.circle(frame, (cX, cY), 2, (0, 0, 0), -1)		# -1 "negative linewidth" is for fill

			# distance calucations
			dis_display = distance(cX-w//2, h//2-cY, altitude)
			cv2.putText(result, dis_display, (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

			# distance vector
			towards_center = vector(w, h, cX-w//2, h//2-cY, df=0.7)				# df: diminishing factor [0, 1]
			cv2.arrowedLine(result, (cX,cY), towards_center, (0,255,255), 1)

			# plot
			x.append(int (altitude * (cX-w//2) / 1000))
			y.append(int (altitude * (h//2-cY) / 1000) )
			z.append(altitude)
			line.set_xdata(x)
			line.set_ydata(y)
			line.set_3d_properties(z)

			line2.set_xdata(x)
			line2.set_ydata(y)

			# x[n] = cX-w//2
			# y[n] = h//2-cY
			# z[n] = altitude
			# line.set_xdata(x[:n+1])
			# line.set_ydata(y[:n+1])
			# line.set_3d_properties(z[:n+1])
			# n += 1

			ax.set_zlim3d(max(0, altitude-500) , altitude+500)

			fig.canvas.draw()
			fig.canvas.flush_events()

			fig2.canvas.draw()
			fig2.canvas.flush_events()


		# frames and altitude text
		cv2.putText(frame, frames, (5, 15),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
		cv2.putText(frame, "altitude: " + str(altitude/100)[:5] + "m" , (5, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

		# displaying
		final_img = cv2.hconcat((frame, result))
		# cv2.imshow("result", result)
		# cv2.moveWindow("result", w, 20)
		cv2.imshow("mask", mask)
		cv2.moveWindow("mask", 0, h+20)
		cv2.imshow("frame", final_img)

		key = cv2.waitKey(1)
		if key == 27:
			break

		# fps measurements
		if i%30 == 0 :
			frames = "FPS: {0:<4.2f} (without realtime plotting ~ 23)".format(i/(time() - t))

		i += 1

	# outside while loop
	plt.show()  # to hold the plot at the end

	cap.release()
	cv2.destroyAllWindows()


main()

