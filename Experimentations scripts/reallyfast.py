import matplotlib.pyplot as plt
import numpy as np
import time
from mpl_toolkits.mplot3d import Axes3D
import psutil

x = [0, 0]
y = [0, 0]
z = [0, 0]

#plot figure with line
fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlim3d(0, 1)
ax.set_ylim3d(0, 100)
ax.set_zlim3d(0,20)
line = ax.plot(x,y,z)[0]

plt.show(block=False)

tstart = time.time()
i = 0
while time.time()-tstart < 60:
  x.append(0.5)
  y.append(i)
  z.append(psutil.cpu_percent())

  line.set_xdata(x)
  line.set_ydata(y)
  line.set_3d_properties(z)

  ax.set_ylim3d(max(0, i-50) , i+50)

  fig.canvas.draw()
  fig.canvas.flush_events()

  i += 1

plt.show()