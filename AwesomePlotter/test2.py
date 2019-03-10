import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from collections import deque
from random import randint, randrange

def get_data():
    '''returns a random amount of random integers'''
    return [1]

points = 200

xdata = np.linspace(0, points, points) # make the X x axis, in this case from -30 to 0
ydata = deque([0]*points, maxlen=points) # initialize the y data with 0's

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
line, = ax1.plot(xdata, ydata, lw=2)

def run(*args):
    ydata.extend(get_data()) # get and add data
    line.set_ydata(ydata) # plot new data
    plt.ylim(min(ydata), max(ydata)) # set limits (use if the data may go off the screen)

ani = animation.FuncAnimation(fig, run, interval=1000) # 20 Hz is 1000//20 ms interval
plt.show()