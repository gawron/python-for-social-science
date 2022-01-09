#!/usr/bin/python

"""
Implementation of Newman's community detection algorithm
see Newman, MEJ (2006) PNAS 103(23):8577-8582.

The original Jacobs University implementaion has been modified and made considerably faster
by Jean Mark Gawron, by basing the computation of the modularity matrix B on matrix
operations rather than the loops in the bg function.  No doubt further efficiencies
are possible.  But it runs well as has been tested on larger graphs
(the polblog graph of Adamic and Glance).

Also added a non recursive split_communities function that just does
a binary split, for convenience.

The community detection seem to work particularly well on the jazz
graph of Gleiser and Danon (2003) and on the admittedly easy
polblogs graph of Adamic and Glance (2005)

By default the community finding functions all incorporate the communities
found as node attributes in the node attribute dictionaries returned with
G.nodes(data=True)
"""

import os.path
import networkx as nx
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from collections import Counter,defaultdict
from networkx_patch import get_biggest_component
from algorithms import spectral_community_detection
import tarfile
import itertools
import operator

def bg(g,i,j,nbunch,verbose=False):
    # returns the modularity matrix for a subset of nodes
    # as defined in Eq. 6 in the paper
    def a(i,j):
      # returns the adjacency matrix element for network g
      if j in g.neighbors(i): return 1
      else: return 0
    def b(i,j):
      #if verbose:
      #   print i,j
      # returns an element of the modularity matrix, defined in Eq. 3 of the paper
      m = len(g.edges())
      return (a(i,j) - 1.0*g.degree(i)*g.degree(j)/(2*m))
    if i == j and len(nbunch) < len(g):
      return b(i,j) - sum([b(i,k) for k in nbunch])
    else:
      return b(i,j)

def klRefine(s,B):
    # Kernighan-Lin refinement, described on pg. 8580
    def flip(v,pos):
      newv = v.copy()
      newv[pos] = -1*v[pos]
      return newv
    def dQ(s2):
      return np.dot(np.dot(s2,B),s2)
    sBest = s
    dQBest = dQ(sBest)
    while True:
      trials = [dQ(flip(sBest,i)) for i in range(len(sBest))]
      if max(trials) > dQBest:
        i = trials.index(max(trials))
        sBest = flip(sBest,i)
        dQBest = dQ(sBest)
      else:
        break
    return sBest

def split(g,nbunch,errorMargin=100,doKL=True,verbose=False,use_bg=False):
    global B, lev
    if verbose:
      print('Computing A')
    m = len(g.edges())
    if use_bg:
        B = np.array([[bg(g,i,j,nbunch,verbose=verbose) for j in nbunch] for i in nbunch])
    else:
        #Always NxN
        #A = nx.to_numpy_matrix(graph)
        A = np.array([[1 if j in g.neighbors(i) else 0 for j in nbunch] for i in nbunch])
        if verbose:
            print('A computed')
        if verbose:
            print('Computing B')
        k = np.array([[g.degree(i) for i in nbunch]])
        kk = k.transpose().dot(k)/(2.0*m)
        B = A - kk
        if len(nbunch) < len(g):
            D = np.diag(np.array([sum([B[i,k_ind] for (k_ind,k) in enumerate(nbunch)]) for i in range(B.shape[0])]))
            B -= D
    if verbose:
      print('B computed')
      print('Computing Eigen vectors')
    w,v = LA.eigh(B) # returns eigenvalues, eigenvectors
    nb1 = []
    nb2 = []
    i = list(w).index(max(w))
    if verbose:
      print('Eigen vectors computed')
    # s as defined on pg. 8579
    #leading eigen vec
    lev = v[:,i]
    s = np.array([(1 if x > 0 else -1) for x in lev])
    # dQ as in eq. 2 and 5
    dQ = np.dot(np.dot(s,B),s)/(4*m)
    if dQ <= errorMargin*np.finfo(np.double).eps:
      return False
    if doKL:
      s = klRefine(s,B)
      dQ = np.dot(np.dot(s,B),s)/(4*m)
    global Q
    Q += dQ
    for j in range(len(s)):
      if s[j] < 0:
        nb1.append(nbunch[j])
      else:
        nb2.append(nbunch[j])
    return (nb1,nb2)

def recursive(g,nbunch,use_bg=False):
    #print nbunch
    nb = split(g,nbunch,use_bg=use_bg)
    #print '   ', nb
    if not nb:
        global resultList
        resultList.append(nbunch)
        return
    else:
        recursive(g,nb[0],use_bg=use_bg)
        recursive(g,nb[1],use_bg=use_bg)

def detect_communities(g,use_bg=False,
                      add_to_node_dict=True):
    global resultList
    resultList = []
    global Q
    Q = 0
    recursive(g,g.nodes(),use_bg=use_bg)  
    if add_to_node_dict:
        add_communities_to_node_dict(g,resultList)
    return Q,resultList

def split_communities(g,use_bg=False,verbose=False,
                      add_to_node_dict=False):
    global resultList
    resultList = []
    global Q
    Q = 0
    resultList = list(split(g,list(g.nodes()),use_bg=use_bg,verbose=verbose))
    if add_to_node_dict:
        add_communities_to_node_dict(g,resultList)
    return Q,resultList

def draw_nodes(g,fileName, communities, prog='neato',use_graphviz=False):
    colorList = [0]*len(g.nodes())
    nodelist = g.nodes()
    for (i,nbunch) in enumerate(communities):
      for n in nbunch:
        #colorList[g.nodes().index(n)] = resultList.index(nbunch)
        colorList[nodelist.index(n)] = i
    plt.figure(figsize=(8,8))
    if use_graphviz:
        pos = nx.graphviz_layout(g,prog=prog)
    else:
        pos = nx.spring_layout(G)
    nx.draw(g,pos,node_color=colorList,with_labels=False)
    plt.savefig(fileName)

def add_communities_to_node_dict(graph, communities, node_dict = None):
    if node_dict is None:
        #node_dict = dict(graph.nodes(data=True))
        node_dict = graph.nodes
    for (i, com) in enumerate(communities):
        for n in com:
            node_dict[n]['Community'] = i
    return node_dict

def call_spectral_community_detection (graph,weighted=False,node_dict=None,
                                       add_to_node_dict=True,binary_split=False):
    """
    graph shd be undirected and connected.
    """
    # Counts the number of edges.  Uses the fact that the graph
    # __get_item__ method iterates through edges.
    # graph[s][e] returns the edge attribute dict for edge (s,e)
    graph_m = dict(list(zip(graph, itertools.count())))
    #inv_indexing = dict((i,n) for (n,i) in graph_m.iteritems())
    inv_indexing = dict(enumerate(graph))
    reindexed_graph = nx.Graph((graph_m[u], graph_m[v]) for (u, v) in
                               graph.edges_iter())
    (modularity, coms) = spectral_community_detection(reindexed_graph, weighted =  weighted,binary_split=binary_split)
    coms = [[inv_indexing[n] for n in com] for com in coms]
    if add_to_node_dict:
        add_communities_to_node_dict(graph,coms)
    return (modularity, coms)
    

def new_draw_nodes(g,fileName,cls_attr='Community',
                   prog = 'neato', pos = None, color_seq = None,
                   val_seq = None,with_labels=False,show=False, title=None,
                   use_graphviz=False):
        """
        Draws graph uses nx drawing tools, which call matplotlib (pyplot) as plt.

        Use color_seq to specify colors used to represent membership in set
        of nodes bearing attribute C{cls_attr}.  By default this is C{Community},
        but it can be any node attribute  represented in C{node_dict}.

        Pass in C{color_seq} to use a particular set of node colors.
        Optionally use val_seq in conjunction to map particular colors to particular values.

        Can optionally pass in a previously computed node layout as C{pos}.  Useful
        for comparing versions of graph colored according to different
        attributes.
        """
        ## Get the range of the attribute function.
        #node_dict = dict(g.nodes(data=True))
        node_dict = g.nodes
        val_set = set([node_dict[n][cls_attr] for n in g.nodes()])
        if color_seq is None:
            # Use integers and default color map
            color_seq = list(range(len(val_set)))
        ## Assign a color index to each member of val_set
        if val_seq is None:
            val_seq = val_set
        else:
            assert(val_set.issubset(val_seq)), 'Data vals include values not in val_seq'
        color_dict = dict((v,color_seq[i]) for (i,v) in enumerate(val_seq))
        colorList = [color_dict[node_dict[n][cls_attr]] for n in g.nodes()]
        plt.figure(figsize=(8,8))
        if title:
            plt.title(title)
        if pos is None and use_graphviz:
            pos = nx.graphviz_layout(g,prog=prog)
            # The next two lines seem to be out of date, since they raise a "Requires pygraphviz" error
            #Gprime = nx.to_agraph(g)
            #Gprime.layout(prog=prog)
        elif pos is None:
            pos = nx.spring_layout(g)
        nx.draw(g,pos,node_color=colorList,with_labels=with_labels)
        plt.savefig(fileName)
        if show:
            plt.show()
        return color_dict, pos


def new_print_purity (g, cls_attr):
    """
    Assumes node_dict has community info represented in a node attribute,
    C{Community}, and that C{cls_attr} is a second node attribute also
    represented in C{node_dict}.
    """
    global communities_dict

    def make_community_dict(g, node_dict):
        nodes = g.nodes()
        communities_dict = defaultdict(list)
        for n in nodes:
            communities_dict[node_dict[n]['Community']].append(n)
        return communities_dict

    def order_keys (keylist):
        try:
            # integer sorting of integer like keys, even if input as strings.
            keylist = sorted([(int(k),k) for k in keylist])
            keylist = [k for (i,k) in keylist]
        except ValueError:
            keylist.sort()
        return keylist

    node_dict = dict(g.nodes(data=True))
    communities_dict = make_community_dict(g, node_dict)
    communities = list(communities_dict.keys())
    ctrs = [Counter(node_dict[n][cls_attr] for n in communities_dict[com])
            for com in communities]
    pop = 0
    for (i,com) in enumerate(communities):
        print(('Com {0: >2d}: {1} members  '.format(i,len(communities_dict[com]))))
        ctr = ctrs[i]
        tot = float(sum(ctr.values()))
        pop += int(tot)
        for cls in order_keys(list(ctr.keys())):
            print(('{0:>20}:  {1:>3d} {2: 7.2%}'.format(cls,ctr[cls],ctr[cls]/tot)))
        print()    
    print(('Total: {0:d}'.format(pop)))

def print_purity (communities, node_dict, cls_attr):
    ctrs = [Counter(node_dict[n][cls_attr] for n in com) for com in communities]
    for (i,com) in enumerate(communities):
        print(('Com {0}: {1} members  '.format(i,len(com))))
        ctr = ctrs[i]
        tot = float(sum(ctr.values()))
        for cls in ctr:
            print(('     class {0}:  {1:>3d} {2: 7.2%}'.format(cls,ctr[cls],ctr[cls]/tot)))
        print()    


def import_dynetmeta_data (filename):
    # The following module is pretty useless.
    # The uselessness of the code is matched only by the uselessness
    # of the "documentation" at
    # http://pythonhosted.org/dynetml2other/

    from dynetml2other import dynetml2other

    # Now wrestle with the religious implications of the
    # dynetml data structure [these folks are a little unclear on
    # the concept of "importing" something into networkx]
    mn = dynetml2other(filename, 'networkx').metanetworks[0]
    # Yes finally an nx graph.  But guess what, no node attributes have been included...
    nx_graph = mn.networks['Agent x Agent']

    # Now we need to add the attributes to the graph.
    # You'd think the mn_node_dict would be what we need, but no not quite....
    _properties,mn_node_dict  = mn._MetaNetwork__node_tree['Agent']['Agent']
    node_dict = dict(nx_graph.nodes(data=True))
    for (n, (meta_dict, prop_dict)) in list(mn_node_dict.items()):
        if n in node_dict:
            node_dict[n].update(prop_dict)
    return nx_graph


################################################################################
## Test code
################################################################################

if __name__ == '__main__':

    # Biggest, most computationally intensive graph in this demo.  Still takes under a minute.
    # Well, not with drawing ...
    polblogs = False
    draw_polblogs = False
    do_lesmis = False
    jazz = True
    timing = True
    #timing = False
    if timing:
        #from timeit import Timer
        import time
    networks_dir = '/Users/gawron/ext/src/sphinx/python_for_ss/ipython_notebooks/network_module/'


    if polblogs:

        polblogpath = os.path.join(networks_dir, "polblogs.gml")

        print('Reading polblogs graph')
        PBG = nx.read_gml(polblogpath)
        print('Graph read')

        #  This loses information, but nothing from now on works without it.
        # Remove selfloops, multiple edges between nodes, prepartory to making it undirected.
        done = set()
        for (start, end) in PBG.edges():
            if start == end:
                PBG.remove_edge(start, end)
                continue
            edge_tup = tuple(sorted((start,end)))
            if edge_tup in done:
                PBG.remove_edge(start, end)
            else:
                done.add(edge_tup)
        PB_UG = PBG.to_undirected()
        big_component = get_biggest_component(PB_UG)
        print(('G: %d nodes  Largest component: %d nodes' % (len(PBG.nodes()), len(big_component.nodes()))))
        if timing:
            print('split_communities')
            t1 = time.time()
            (polblog_modularity,polblog_communities) =\
                                    split_communities(big_component)
            t2 = time.time()
            print(('{0:.3f} secs; modularity {1:.4f} {2:d} communities'.format(t2 - t1,polblog_modularity,len(polblog_communities))))
            print()
            print('call_spectral_communities')
            t1 = time.time()
            (polblog_modularity0,polblog_communities0) =\
                           call_spectral_community_detection(big_component,
                                                             binary_split=True)
            t2 = time.time()
            print(('{0:.3f} secs; modularity {1:.4f} {2:d} communities'.format(t2 - t1,polblog_modularity0,len(polblog_communities0))))
        else:
            (polblog_modularity,polblog_communities) = \
                           split_communities(big_component,verbose=True)
        print(("Ploblogs Q = ", polblog_modularity))

        new_print_purity (big_component, 'value')
        if draw_polblogs:
            print('Drawing Polblogs')
            # SFDP one of 3 spring layout algorithms in graphviz (also neato and fdp)
            # This multilevel algorithm is recommended for larger graphs.
            # For sfdp examples see http://yifanhu.net/GALLERY/GRAPHS/index.html
            # SFDP APPEARS to give the same layout on every run.  Detr
            draw_nodes(big_component,"polblogs.png", polblog_communities, prog='sfdp')
            print('Polblogs drawn')

    # Just split a graph in two
    g2 = nx.karate_club_graph()
    (modularity,communities) = split_communities(g2)
    print(("Karate club Q = ", modularity))
    # refers to global resultList for coloring.
    #draw_nodes(g2,"karate_club.png", communities)
    kclub_color_dict, kpos = new_draw_nodes(g2,"karate_club.png", cls_attr = 'Community', prog='fdp',color_seq=['Cyan', 'Gold'], with_labels = True, show = True, title = 'Karate Club Communities')

    archive = tarfile.open("meb/utils/network/tests/real_world_networks.tar.bz2", mode="r:bz2")
    graph = nx.read_gml(archive.extractfile("networks/dolphins-newman-2003.gml"))
    ##### DOLPHIN A Find best community partition.
    (d_modularity,d_communities) = detect_communities(graph)
    print(("Dolphin communities Q = ", d_modularity))
    d_community_color_dict, pos = new_draw_nodes(graph,"dolphin_communities.png", cls_attr = 'Community', prog='fdp',color_seq=['Aqua','Ivory','Blue', 'Gold', 'DarkGray'],show=False ,title='Dolphin communities')

    ##### DOLPHIN B Experimenting with a binary split
    (ds_modularity,ds_communities) = split_communities(graph)
    print(("Dolphin split Q = ", ds_modularity))
    # Dolphin 36 [label = 'SN100'] is the keystone dolphin drawn
    # in Newman (2006) Physical review E, Fig. 2.
    # Source: Lusseau & Newman (2004) [NOT Lusseau et al (2003) as stated on
    # Newman's network data page]
    # The only node of degree 7 with  2 cross community connections,
    # according to the algorihtm's split.
    # But None of the obvious manipulations of leading eigenvector (C{lev})
    # pick him out. For example
    support_points = sorted(enumerate(lev), key=lambda x: abs(x[1]))
    # Find node with min abs value in eigen vector.
    min_index, min_value = support_points[0]
    # nor does max, min, max o abs work But SN100 DOES have high
    # betweenness, according to Lusseau & Newman (2004)
    #draw_nodes(graph,"dolphin_communities.png", d_communities)
    # Color seq can be longer than list of coms found, but not shorter.
    ds_community_color_dict, pos = new_draw_nodes(graph,"dolphin_split.png", cls_attr = 'Community', prog='fdp',color_seq=['Aqua','Ivory'],with_labels=True,show = True, title='Dolphins: binary community split')



    if jazz:
        print('Reading jazz graph')
        Jazz = nx.read_edgelist('jazz.el',comments='%')
        print('Jazz Graph read')
        Jazz_UG = Jazz.to_undirected()
        Jazz_BC = get_biggest_component (Jazz_UG)

        #(modularity,communities) = detect_communities(Jazz_BC)
        (jz_modularity,jz_communities) = \
                               call_spectral_community_detection (Jazz_BC)
        print(("Jazz network Q = ", jz_modularity))
        jz_community_color_dict, pos = new_draw_nodes(Jazz_BC,"jazz_graph.png", cls_attr = 'Community', prog='fdp',color_seq=['Cyan','DarkGray','DarkSalmon','Gold'], show = True, title = 'Jazz Communities')
        #draw_nodes(Jazz_graph,"jazz_graph.png", communities, prog='sfdp')


    if do_lesmis:
        lesmispath = os.path.join(networks_dir, "lesmiserables.gml")
        print('Reading les mis graph')
        lesmis = nx.read_gml(lesmispath)
        print('Graph read')
        lesmis_UG = lesmis.to_undirected()
        (modularity,communities) = detect_communities(lesmis_UG)
        draw_nodes(lesmis_UG,"lesmis_graph.png", communities, prog='sfdp')

    # Goodreau's Faux Mesa High school  data
    # "A simulation of an in-school friendship network."
    # http://www.casos.cs.cmu.edu/computational_tools/datasets/external/Goodreau/index11.php
    print('Reading Faux Mesa High graph')
    fmhs_nx_graph = import_dynetmeta_data ('FauxMesaHigh.xml')
    print('Faux Mesa High graph read')

    fmhs_nx_graph_UG = fmhs_nx_graph.to_undirected()
    fmhs_big_component = get_biggest_component(fmhs_nx_graph_UG)

    (fmhs_modularity,fmhs_communities) = \
                               detect_communities(fmhs_big_component)
    print(("FMHS Q = ", fmhs_modularity))

    # In fact DONT see much assortative mixing by RACE, at least if these are real communities.
    new_print_purity (fmhs_big_component, 'Race')

    community_color_dict, pos = \
           new_draw_nodes(fmhs_big_component,"fmhs_community_graph.png",
                          cls_attr = 'Community', prog='fdp', show = True, title = 'Faux Mesa HS Communities')
    race_color_dict, pos = \
          new_draw_nodes(fmhs_big_component,"fmhs_race_graph.png",
                         cls_attr='Race', prog='fdp', pos=pos,
                         color_seq=['dimgray','coral','burlywood','ivory'],
                         val_seq=['Black','NatAm','Hisp','White'], show = True, title = 'Faux Mesa HS Races')

    gender_color_dict, pos = \
          new_draw_nodes(fmhs_big_component,"fmhs_gender_graph.png",
                         cls_attr='Sex', prog='fdp', pos=pos,
                         color_seq=['cyan','pink'],
                         val_seq=['M','F'], show = True, title = 'Faux Mesa HS Sexes')


    ## Political books.Valdis Krebs (http://www.orgnet.com/, downloaded off Mark Newman's network data page:  http://www-personal.umich.edu/~mejn/netdata/
    pol_book_graph = nx.read_gml('polbooks.gml')
    #pol_book_node_dict = dict(pol_book_graph.nodes(data=True))
    #(pol_book_modularity,pol_book_communities) = detect_communities(pol_book_graph)
    (pol_book_modularity,pol_book_communities) = \
             call_spectral_community_detection(pol_book_graph,
                                               weighted=False)

    new_print_purity (pol_book_graph, 'value')


    community_color_dict, pos = \
            new_draw_nodes(pol_book_graph,"pol_book_graph.png",
                           cls_attr = 'Community', prog='fdp', show = True, title = 'Pol Book Communities')
    orientation_color_dict, pos = \
            new_draw_nodes(pol_book_graph,"pol_book_orientation_graph.png",
                           cls_attr='value', prog='fdp', pos=pos,
                           color_seq=['red','blue','white'],
                           val_seq=['l','c','n'], show = True, title = 'Pol Book Political Orientations')
