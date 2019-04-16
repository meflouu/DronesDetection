# import numpy as np
# import matplotlib.pyplot as plt

# plt.axis([0, 10, 0, 1])

# for i in range(1000):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.05)

# plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
line, = ax.plot(x, y, color='k')

def update(num, x, y, line):
  line.set_data(x[:num], y[:num])
  line.axes.axis([0, 10, 0, 1])
  return line,

ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line], interval=25, blit=True)
plt.show()