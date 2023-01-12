"""
This runs from a terminal but not in a jupyter NB.

Might want to try Goigle colab.
"""

from random import randint

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# function that draws each frame of the animation
def animate(i):
    pt = randint(1,9) # grab a random integer to be the next y-value in the animation
    x.append(i)
    y.append(pt)

    ax.clear()
    ax.plot(x, y)
    ax.set_xlim([0,20])
    ax.set_ylim([0,10])

# create empty lists for the x and y data
x = []
y = []

# create the figure and axes objects
fig, ax = plt.subplots()


# run the animation
ani = FuncAnimation(fig, animate, frames=20, interval=500, repeat=False)
#ani.save("mp4")
plt.show()
