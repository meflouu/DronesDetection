import time
import psutil
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib import style
import psutil

style.use('seaborn')

xline = []
yline = []
zline = []

def animate(i):
  xline.append(float(psutil.cpu_percent()) + 2)
  yline.append(float(psutil.cpu_percent()) + 5)
  zline.append(float(psutil.cpu_percent()))

  ax.clear()
  ax.set_ylim3d(max(0, i-50) , i+50)
  ax.plot3D(xline, yline, zline, color='violet', linewidth=1)




# figure initliaztion
fig = plt.figure()
ax = Axes3D(fig)
# ax.set_xlim3d(-1000, 1000)
# ax.set_ylim3d(-1000, 1000)
# ax.set_zlim3d(0,5500)

ani = animation.FuncAnimation(fig, animate, interval=30, blit=False)

plt.show()