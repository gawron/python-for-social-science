"""
From
http://wiki.scipy.org/Cookbook/Matplotlib/Interactive_Plotting

Simple example::

    x = range(10)
    y = range(10)
    annotes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    scatter(x,y)
    af =  AnnoteFinder(x,y, annotes)
    connect('button_press_event', af)

Adding linked annotation finders onto
an existing one::

    subplot(121)
    scatter(x,y)
    af1 = AnnoteFinder(x,y, annotes)
    connect('button_press_event', af1)

    subplot(122)
    scatter(x,y)
    af2 = AnnoteFinder(x,y, annotes)
    connect('button_press_event', af2)

    linkAnnotationFinders([af1, af2])

"""

import math

import pylab
import matplotlib


class AnnoteFinder:
  """
  callback for matplotlib to display an annotation when points are clicked on.  The
  point which is closest to the click and within xtol and ytol is identified.
    
  Register this function like this:
    
  scatter(xdata, ydata)
  af = AnnoteFinder(xdata, ydata, annotes)
  connect('button_press_event', af)
  """

  def __init__(self, xdata, ydata, annotes, axis=None, xtol=None, ytol=None):
    self.data = zip(xdata, ydata, annotes)
    if xtol is None:
      xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
    if ytol is None:
      ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
    self.xtol = xtol
    self.ytol = ytol
    if axis is None:
      self.axis = pylab.gca()
    else:
      self.axis= axis
    self.drawnAnnotations = {}
    self.links = []

  def distance(self, x1, x2, y1, y2):
    """
    return the distance between two points
    """
    return math.hypot(x1 - x2, y1 - y2)

  def __call__(self, event):
    if event.inaxes:
      clickX = event.xdata
      clickY = event.ydata
      if self.axis is None or self.axis==event.inaxes:
        annotes = []
        for x,y,a in self.data:
          if  clickX-self.xtol < x < clickX+self.xtol and  clickY-self.ytol < y < clickY+self.ytol :
            annotes.append((self.distance(x,clickX,y,clickY),x,y, a) )
        if annotes:
          annotes.sort()
          distance, x, y, annote = annotes[0]
          self.drawAnnote(event.inaxes, x, y, annote)
          for l in self.links:
            l.drawSpecificAnnote(annote)

  def drawAnnote(self, axis, x, y, annote):
    """
    Draw the annotation on the plot
    """
    if (x,y) in self.drawnAnnotations:
      markers = self.drawnAnnotations[(x,y)]
      for m in markers:
        m.set_visible(not m.get_visible())
      self.axis.figure.canvas.draw()
    else:
      #t = axis.text(x,y, "(%3.2f, %3.2f) - %s"%(x,y,annote), )
      t = axis.text(x,y, "%s"%(annote,), bbox = dict(boxstyle = 'round,pad=0.15', fc = 'salmon', alpha = .75))
      m = axis.scatter([x],[y], marker='d', c='r', zorder=100)
      self.drawnAnnotations[(x,y)] =(t,m)
      self.axis.figure.canvas.draw()

  def drawSpecificAnnote(self, annote):
    annotesToDraw = [(x,y,a) for x,y,a in self.data if a==annote]
    for x,y,a in annotesToDraw:
      self.drawAnnote(self.axis, x, y, a)


############################################################
############################################################
##
##
##
##
##
############################################################
############################################################


      

def linkAnnotationFinders(afs):
  for i in range(len(afs)):
    allButSelfAfs = afs[:i]+afs[i+1:]
    afs[i].links.extend(allButSelfAfs)


if __name__ == '__main__':

    """
    A demo with a Facebook ego network
    """

    import networkx as nx
    import matplotlib.pyplot as plt
    import pylab

    ego_network = nx.read_gml('samraj_network_anon.gml',relabel=True)
    #ego_network = nx.read_gml('homer.gml',relabel=True)

    ego_pos = nx.spring_layout(ego_network,scale=1.0,iterations=500)
    ego_il = ego_pos.items()

    labels = [label for (label,coords) in ego_il]
    X = [x for (label,(x,y)) in ego_il]
    Y = [y for (label,(x,y)) in ego_il]
    
 
    #nx.draw_networkx(ego_network,ego_pos)
    nx.draw_networkx_edges(ego_network,ego_pos)
    af =  AnnoteFinder(X,Y, labels)
    pylab.connect('button_press_event', af)
    plt.show()
    
