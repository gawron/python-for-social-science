import networkx as nx
import matplotlib.pylab as plt
import matplotlib.cbook as cb
import math

def annotate_with_networkx_labels(G, pos,
                                  labels = None,
                                  fontname = 'Arial',
                                  font_size = 12,
                                  font_color = 'k',
                                  font_weight = 'normal',
                                  alpha = 1.0,
                                  ax = None,
                                  horizontalalignment = 'center',
                                  verticalalignment = 'center',
                                  xoff = 0.0,
                                  yoff = 0.0,
                                  offset_dict = None,
                                  **kwds):
    """
    Has much of the functionality of draw_networkx_labels but uses matplotlib's
    text annotation function to allow fine-tuning of label positions.  Adds
    the capability of specifying default node x- and y- offsets to control
    positioning of label with respect to nodes.  Also provides an optional
    offset dict which allows offset positions to be stipulated node by node.
    Nodes not mentioned in the offset dict take the default offsets.

    The label dict is the usual networkx label dict, a mapping
    from node names/indices to labels. Can also be used to abbreviate labels
    when layout crowds nodes together.

    Draw node labels on the graph G.

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See networkx.layout for functions that compute node positions.

    font_size : int
       Font size for text labels (default=12)

    font_color : string
       Font color string (default='k' black)

    font_weight : string
       Font weight (default='normal')

    xoff: int ot float
        Horizontal offset in points of text from node
        
    yoff: int ot float
        Vertical offset in points of text from node
        
    alpha : float
       The text transparency (default=1.0)

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.
    """
    if ax is None:
        ax=plt.gca()

    if labels is None:
        labels=dict( (n,n) for n in G.nodes())

    # A variant for some of the text annotations.
    text_props_r = dict(fontname = fontname,
                        size = font_size,
                        color = font_color,
                        weight = font_weight,
                        verticalalignment = verticalalignment,
                        horizontalalignment = horizontalalignment,
                        alpha = alpha,
                        # Express text coords in offsets from xy, unit is pt
                        textcoords ='offset points')
    text_props_r.update(kwds)
    text_items={}  # there is no text collection so we'll fake one
    offset_dict0 = dict((n,(xoff,yoff)) for n in G)
    if offset_dict:
        offset_dict0.update(offset_dict)
    for n, label in list(labels.items()):
        (x,y)=pos[n]
        if not cb.is_string_like(label):
            label=str(label) # this will cause "1" and 1 to be labeled the same
        thisxoff,thisyoff = offset_dict0[n]
        t=ax.annotate(label,xy=(x, y),
                      xytext=(thisxoff,thisyoff),
                      #transform = ax.transData,
                      clip_on=True,
                      **text_props_r
                      )
        text_items[n]=t

    return text_items


def assign_colors(G, color_att, color_seq=None, val_seq=None, integers_ok=True):
   node_dict = G.node
   val_set = set([node_dict[n][color_att] for n in G.nodes()])
   if color_seq is None and integers_ok:
         # Use integers and default color map
         color_seq = list(range(len(val_set)))
   elif color_seq is None:
         color_seq = ('red','cyan','dimgray','coral','burlywood','ivory','k')
   if val_seq is None:
      val_seq = val_set
   else:
       assert(val_set.issubset(val_seq)), 'Data vals include values not in val_seq'
   assert len(val_seq) <= len(color_seq), \
     'Not enough colors available ({0}) for valueset size ({1}). Specify more.'.format(len(color_seq),
       len(value_seq))
   return dict(list(zip(val_seq, color_seq)))



def write_color_dot_file (G,color_att=None, del_atts=None, dot_file='dot_graph.dot',
                          node_color=None,color_seq=None,val_seq=None,label=True):
      if del_atts is None:
         del_atts = []

      if node_color is None:
          color_dict = assign_colors(G, color_att, color_seq,val_seq,integers_ok=False)
      else:
          assert color_att is None, 'Please do not specify a color attribute and a single node color at the same time'

      for (n,ndict) in G.node.items():
          ndict['style'] = 'filled'
          if node_color:
              ndict['fillcolor'] =  node_color
          else:
              ndict['fillcolor'] = color_dict[ndict[color_att]]
          if not label:
                ndict['label'] = '""'            
          for del_att in del_atts:  
             try:
               del ndict[del_att]
             except KeyError:
               continue
      nx.write_dot(G, dot_file)

def draw_color_graphviz_graph (G, color_att, pos=None, labels=None,
                               prog='sfdp', offset_dict=None, yoff=8,
                               plt_file=None, node_size=220, node_alpha=.9,
                               label_alpha=.8, edge_alpha = .3,
                               node_color = None, color_seq=None,
                               val_seq=None, label=True):

   """
   node_color can be a be a color string spec; if it is, all nodes get that
   color.
   """
   node_dict  = G.node
   if node_color is None:
      color_dict = assign_colors(G, color_att, color_seq,val_seq)
      # List of length n (# nodes) that assigns a color to each node
      colorList = [color_dict[node_dict[n][color_att]] for n in G.nodes()]
   else:
      ColorList = node_color
   plt.figure(figsize=(11,11))
   if pos is None:
       pos = nx.graphviz_layout(G,prog = prog)
   nx.draw_networkx_nodes(G,pos,
                          node_color=colorList,
                          node_size=node_size,
                          alpha=node_alpha)
   nx.draw_networkx_edges(G,pos,width=.8,alpha=edge_alpha)
   if label:
      annotate_with_networkx_labels(G,pos,labels=labels,yoff=yoff,
                                    alpha = label_alpha,
                                    verticalalignment='bottom',
                                    offset_dict = offset_dict) 
   if plt_file:
      plt.savefig(plt_file)


