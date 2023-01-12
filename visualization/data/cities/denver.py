import os.path
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)
width,height = 60000,42500

# Denver -105.07,39.76  # lat comes second! The plot is shifted a little
# East of Denver’s center because of it’s weird shape.
map = Basemap(resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = -104.9,
              width=width,height=height)
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#ddaa66',lake_color='aqua’)
# This is the key
map.drawcounties()
# Just to demonstrate superimposing a plot.
x = np.linspace(0,width,200)
plt.plot(x,x)
plt.show()
