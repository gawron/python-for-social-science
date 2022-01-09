"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

#plt.subplot(#row,#cols,current)
fig,axes = plt.subplots(nrows = 1, ncols=2)
ax0, ax1 = axes
ax0.plot(x1, y1, 'yo-')
plt.title('A tale of 2 subplots')
ax0.set_ylabel('Damped oscillation')

#plt.subplot(2, 1, 2)
ax1.plot(x2, y2, 'r.-')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Undamped')

plt.show()
