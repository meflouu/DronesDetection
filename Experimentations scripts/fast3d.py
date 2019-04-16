import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import psutil

# pre alloacted lists
x = [None] * int(5000)
y = [None] * int(5000)
z = [None] * int(5000)

def update(i, x, y, z):
	x[i] = 1
	y[i] = i
	z[i] = psutil.cpu_percent()

	ax.set_ylim3d(max(0, i-50) , i+50)
	ax.plot3D(x[max(0, i-2):i], y[max(0, i-2):i], z[max(0, i-2):i], color='violet', linewidth=1)
	return ax,

# figure initliaztion
fig = plt.figure()
ax = Axes3D(fig)

ani = animation.FuncAnimation(fig, update, fargs=[x, y, z], interval=25, blit=True)

plt.show()