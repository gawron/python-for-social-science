#import community
import os.path
wd = '/Users/gawron/ext/src/sphinx/python_for_ss/ipython_notebooks/'
os.chdir(wd)
import louvain
import networkx as nx
import matplotlib.pyplot as plt
from itertools import cycle

def get_partition_coloring (G, partition):
    ## Cycle through the colors once again if there
    ## are too many partitions.
    colors = cycle('bgrcmyk')
    partitions = set(partition.values())
    color_map = dict(zip(partitions, colors))
    return [color_map[partition[n]] for n in G.nodes()]


#######################################################################
##
##                 R e a d i n g    G r a p h
##    (making it undirected, finding biggest connected component)
##
#######################################################################


wd = '/Users/gawron/ext/src/sphinx/python_for_ss/ipython_notebooks/'
G = nx.read_gml(os.path.join(wd,'polblogs.gml'))

# Remove selfloops
for (start, end) in G.edges():
    if start == end:
        G.remove_edge(start, end)
und_G0 = G.to_undirected()

# For some reason the type of this is still a multigraph, so louvain aborts.
# Sledge hammer time
und_G1 = nx.Graph(data=list(set(und_G0.edges())))
# Might as well just do the large connected component while were at it.
components = nx.connected_components(und_G1)
und_G = nx.subgraph(und_G1,components[0])

#######################################################################
##
##           F i n d i n g       C o m m u n i t i e s
##
#######################################################################


#partition = community.best_partition(und_G)
partition = louvain.best_partition(und_G)

#######################################################################
##
##                     D r a w i n g
##
#######################################################################

colors = get_partition_coloring(und_G,partition)
pos = nx.spring_layout(und_G)
#count = 0.
nx.draw_networkx_nodes(und_G, pos, und_G.nodes(), node_size = 80,
                                node_color = colors)
nx.draw_networkx_edges(und_G,pos, alpha=0.5)
plt.show()

