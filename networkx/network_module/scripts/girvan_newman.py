import networkx as nx
import math
from collections import defaultdict,Counter

def girvan_newman (G, print_biggest = False, max_d=None,min_size=None,min_component_ratio=.1,
                   create_partition=False,relabel_partition_flag=False):
    """
    A very simple no bells and whistles implementation of
    girvan-newman, relying on networkx.


    Returns a C{components_dict}.  This is a dictionary with form
    C{component_id} => (C{c1}, C{c2}) where C{component_id} is the string id of
    a graph component, and C{c1} and C{c2} are the
    two subcomponents of C{component_id}, represented as node lists.
    String ids are assigned according to the following convention:
    The string id of C{c1} is C{component_id} +'0' and the  string_id
    of C{c2} is C{component_id} + '1'.  The string id of the largest connected
    component of C{G} is '0'.  Thus the longer a string id, the more deeply
    embedded if is in Girvan-Newman's recursive computation.  We order
    C{c1} and C{2} in the pair (C{c1},C{c2}) so that len(C{c1}) > len(C{c2}).

    Since this destroys the graph, we make a copy of the graph
    at the top level, using::

       G.copy()


    """
    G = G.copy()
    components_dict = defaultdict(list)
               
    index = '0'


    big_component = max(nx.connected_component_subgraphs(G),key=lambda x: len(x.nodes()))
    bg_len = len(big_component.nodes())
    if min_size is None:
        min_size = math.floor(min_component_ratio * bg_len)

    print('G size: %d Max component size: %d min splittable size: %d' % (len(G.nodes()),bg_len,min_size))

    girvan_newman_helper(big_component, print_biggest = print_biggest, index = '0',
                         max_d = max_d, components_dict=components_dict,min_size=min_size,
                         create_partition=create_partition)
    print('Creating partition: %s' % create_partition)
    if create_partition:
        #return partition_components_dict(G,components_dict,min_partition_size=min_size)
        partition =  partition_components_dict(G,components_dict)
        ps = set(partition.values())
        print('Partitions found', end=' ')
        print(ps)
        if relabel_partition_flag:
            partition = relabel_partition(G, partition)
        return partition
    else:
        return components_dict


def girvan_newman_helper (G, print_biggest = False, index='0',
                          max_d=None,components_dict=None,min_size=100,
                          create_partition=False):
    
    # print 'index: %s (%d nodes) => ' % (index,len(G.nodes())),

    if len(G.nodes()) == 1:
        components_dict[index].append(G.nodes())
        return components_dict
    
    def find_best_edge(G0):
        """
        Networkx implementation of edge_betweenness
        returns a dictionary. Make this into a list,
        sort it and return the edge with hoghest betweenness.
        """
        eb = nx.edge_betweenness_centrality(G0)
        eb_il = list(eb.items())
        eb_il.sort(key=lambda x: x[1], reverse=True)
        return eb_il[0][0]

    components = list(nx.connected_component_subgraphs(G))
    
    while len(components) == 1:
        G.remove_edge(*find_best_edge(G))
        components = list(nx.connected_component_subgraphs(G))

    # for later, put big component first.
    
    components.sort(key=lambda x: len(x.nodes()),reverse=True)
    for c in components:
        print('%d nodes' % (len(c.nodes()),), end=' ')
    print()

    for c in components:
        components_dict[index].append(tuple(c.nodes()))
    if print_biggest:
        for c in components_dict[index]:
            print(c)
    if (max_d is None) or (len(index) < max_d):
        ctr = 0
        for c in components:
            if len(c.nodes()) > min_size:
                girvan_newman_helper(c,index='%s%d' % (index,ctr),
                                     max_d=max_d,components_dict=components_dict,min_size=min_size)
            ctr += 1
    return components_dict

def relabel_partition (G, partition):
    new_partition = dict()
    nds_dict = dict(G.nodes(data=True))
    for (k,v) in partition.items():
        new_partition[nds_dict[k]['label']] = v
    return new_partition
    

def find_big_splits  (components_dict):
    """
    Assumes Girvan Newman (GN) has been run with a min_size val that excludes
    components of very small size, so that all splits are of interest.  Also
    assumes the components dict GN produces has the structure cluster_id => (c1,c2),
    where len(c2) > len(c1).

    Then just sorts the list of splits by the size ratio (if c splits as c1,c2, then c1/c2), and
    returns that sorted list.  First thing on it shd be the best "interesting component" split

    """
    def get_ratio (entry):
        try:
            (index, (c1,c2)) = entry
        except:
            return 0
        return float(len(c1))/len(c2)
    components_dict_il = list(components_dict.items())
    rl = [(get_ratio(x),x[0],len(x[1][0]),len(x[1][1])) for x in components_dict_il if len(x[1]) == 2]
    return sorted(rl)


def old_find_big_split  (components_dict, ratio_limit=1.6,min_diameter=0):
    global component_size,victors
    assert ratio_limit > 1, 'Must use a ratio limit greater  than 1'
    ratio_limit_inverse = 1/ratio_limit
    components_dict_il = list(components_dict.items())
    components_dict_il.sort(key=lambda x: len(x[0]))
    
    #size = len(G.nodes())
    big_components = components_dict['0']
    size = len(big_components[0]) + len(big_components[1])
    depth = 1
    target_split_diameter = size
    component_size = {'0':size}
    victors = set()
    # Put larger component first in each partition.
    while (target_split_diameter > min_diameter) and not victors:
        # Extract all victors meeting ratio requirement and bigger
        # than target_split_diameter on this round of while loop.
        # If none found we'll try again with reduced target_split_diameter
        best_split_diameter = 0
        for entry in components_dict_il:
            print('for1: ', target_split_diameter, best_split_diameter, depth)
            try:
                (index,(c1,c2)) = entry
            except ValueError:
                continue
            print(index)
            if len(index) > depth:
                if 0 < best_split_diameter < target_split_diameter:
                    ## It keeps getting smaller from here
                    ## so give up and reduce target
                    break
                if victors:
                    break
                depth = len(index)
                best_split_diameter = 0

            if component_size[index] > best_split_diameter:
                best_split_diameter = component_size[index]

            ## Record component sizes of compnents for future ref
            c1_len, c2_len = (len(c1),len(c2))
            component_size[index + '0'] = c1_len
            component_size[index + '1'] = c2_len
            
            if component_size[index] >= target_split_diameter:
                this_ratio = float(c1_len)/c2_len
                if (ratio_limit > this_ratio):
                    victors.add((c1,c2))
               
                
        target_split_diameter -= 1
    return argmax (victors)

    
def argmax (victors):
    if len(victors) > 1:
        f = lambda x: max(len(x[0]),len(x[1]))
        return max(victors,key = lambda x: f(x))
    else:
        return victors


def get_cluster_purity (G, clusters, class_att):
    """
    C{clusters} is a list of node lists, each representing
    a cluster in the original graph C{G}. C{class_att} is the classifying attribute
    of interest, which must be a key in  all the node dicts for nodes in graph C{G}.

    Returns C{purity_list}: C{purity_list[component_index]} => (value, purity_score,size)
    For each cluster ci in clusters, return a triple of (i) the value of C{class_att}
    held by majority of members of ci; (ii) percentage of members of ci having that value;
    and (iii) size of ci.
    """
    node_dict = dict(G.nodes(data=True))
    purity_list = []
    for (i,clust) in enumerate(clusters):
        att_dict = Counter()
        size = len(clust)
        for n in clust:
            att_dict[node_dict[n][class_att]] += 1
        (winning_class,winning_class_ct) = att_dict.most_common()[0]
        purity_list.append((winning_class,float(winning_class_ct)/size,size))
    return purity_list


def partition_components_dict(G,components_dict,min_partition_size=2):
    """
    This is not yet right.

    Let's say we know when to say cluster c_k has significant components c1,c2
    based on some correct definition of C{passes_test} below.

    We still need a criterion for when we can replace c1,c2, or both
    by THEIR components.  So if it's both, then part_dict[c_k] = union(parts_dict[c1],parts_dict[c2]).

    Just saying whenEVER c2 or c2 have components always favors smaller components.
    Saying NEVER always favors smaller components.

    Let's c_k is a significant component of c_m.
    When are c_k's componets, c1,c2,...cn (size_sorted) a good replacement for ck as components of c_m.
    One answer:
    
    passes_test(size_dict[c_n],len(c_m),N,min_partition_size)

    We may pass the test, but why would c1,...cn be a better answer than c_k,
    which is BIGGER?  It cant be information loss.  BY our current criteria
    it can only be because c_k is still too big, and is better broken up.
    But this function call cant apply that criterion...

    """
    print('Calling partition_components')
    N = len(G.nodes())
    components_dict = components_dict.copy()
    components_dict_il = list(components_dict.items())
    size_dict = dict()
    for entry in components_dict_il:
        try:
            (k,(c1,c2))  = entry
        except:
            continue
        size_dict[k] = len(c1) + len(c2)
    components_dict_il = [(k, (c1,c2)) for (k, (c1,c2)) in components_dict_il if k in size_dict]
    components_dict_il.sort(key=lambda x: size_dict[x[0]],reverse=True)
    #print len(size_dict), len(components_dict_il), len(components_dict)

    def passes_test(c_size,M,N,min_partition_size,r):
        """
        This is not yet right.
        :"""
        if  c_size < min_partition_size or r > 6.0:
            return False
        else:
            return True
        #  None of the other criteria detailed below are beiung used yet.
        #  M Not too big relative to N and cluster not too small relative to M
        test = M < (.8 * N) and  r <= 9.0 # 1.6
        if test:
            return True
        elif  M < (.8 * N):
            # M  not too big.
            return r < 2.0
        elif r < 8:
            # M is too big. split it.
            return True
        else:
            return False

    # parts_dict the topdown correspondent to the partition_dict
    # Start with every node assigned to an "other" partition
    parts_dict,partition_dict = (defaultdict(list),dict(list(zip(G.nodes(),N*['1']))))
    for (k, (c1,c2)) in components_dict_il:
        parts_dict[k] = [c1,c2]
        c1_len,c2_len = (len(c1),len(c2))
        #print len(c2), size_dict[k],N,min_partition_size,c1_len,c2_len
        if passes_test(len(c2),size_dict[k],N,min_partition_size,float(c1_len)/c2_len):
            update_partition_dict(k,(c1,c2),parts_dict,partition_dict)
        #elif c1 in parts_dict:
        #    if test_cluster_parts(k,size_dict[k],N, [c1,c2],partition_dict,parts_dict,components_dict,size_dict):
        #        update_partition_dict(k,size_dict[k],N,parts_dict[c1],
        #                              partition_dict,parts_dict,components_dict,size_dict)
    return partition_dict

    
def update_partition_dict (k,component_nodes,parts_dict,partition_dict):
    #for (i,c) in enumerate(components):
    for i in range(len(component_nodes)):
        parts_dict[k].append('%s%d' % (k,i))
        for n in component_nodes[i]:
            partition_dict[n] = k
        

    
if __name__ == '__main__':

    import os.path
    os.chdir('/Users/gawron/ext/src/sphinx/python_for_ss/ipython_notebooks')
    to_do = 'polblog'
    #to_do = 'zachary'
    #to_do = 'samraj_network'

    if to_do == 'polblog':
        
        pb = nx.read_gml('polblogs.gml').to_undirected()
        #components = girvan_newman(pb, print_biggest=True)
        print('Running girvan newman')
        # first split:  1218, 4 ... continues in this fashion for QUITE a long time...
        components_dict = girvan_newman(pb, print_biggest=False)
        print('girvan newman run')


        # Rank according to ratio of sizes of cluster components, smallest ratio to biggest.

        ratio_list  = find_big_splits(components_dict)
        #  For the polblogs graph the split ranked highest by size ratio is the "interesting split",
        #  len1=556,len2=437, accoiunting for 993 members
        #  (81%) of the 1222 members of the largest connected component of the original polblog grap pb.
        #  Note that's only (66.6%) of the original 1490 members of pb.
        (ratio, winner, len1, len2) = ratio_list[0]
        purity = get_cluster_purity(pb,components_dict[winner],'value')
        ########  For polblog only  ##########################################
        # Going UP the hierarchical clustering tree produced by girvan-newman,  we will of
        # course get "small" split off clusters with BOTH values for "value". For example
        #purity2 = get_cluster_purity(pb,components_dict[winner[:-1]],'value')
        #print purity2
        #print 'This is the purity calculation for  the "parent" cluster of "winner".'
        #print 'THe first cluster has terrible purity because it is of course our "winner", which is close to 50/50.'
        #print 'Note the singleton node split off has value 0'
        #purity3 = get_cluster_purity(pb,components_dict[winner[:-2]],'value')
        #print purity3
        #print 'This is the purity calculation for the parent of the parent of "winner".'
        #print 'Note that this time the singleton node split off has value 1'

        X = """
        Speculation:  The small clusters of nodes being split off from the ancestors of C{winner}
        are all in the thin "middle" part of the barbell shape we see in Gephi after running the force-directed
        layout algorithm.  We are recovering the rounded "ends" of the barbell in C{winner}.
        """

        print(X)
    
    ################################################################################################
    ################################################################################################
    #        Z a c h a r y     K a r a t e
    ################################################################################################
    ################################################################################################

    if to_do == 'zachary':
        kn = nx.karate_club_graph()
        z_components_dict = girvan_newman(kn, print_biggest=False)
        z_ratio_list  = find_big_splits(z_components_dict)
        # For Zachary's karate the interesting split is the top split '0', which comes second on the ratio list
        (z_ratio, z_winner, z_len1, z_len2) = z_ratio_list[1]
        # The Officer cluster only has purity 89.5%, while the Mr. Hi faction has purity 100%
        # There are 2 Mr. Hi nodes tangled up among the others.
        z_purity = get_cluster_purity(kn,z_components_dict[z_winner],'club')
        # Going one level deeper doesnt help. An officer node is split off, not a Mr. Hi node as one might hope.
        z_purity2 = get_cluster_purity(kn,z_components_dict[z_winner+'0'],'club')
        # Going one level further doesnt help either. We get two substantial sub factions,
        # each with one Mr. Hi node.
        z_purity3 = get_cluster_purity(kn,z_components_dict[z_winner+'00'],'club')

    ################################################################################################
    ################################################################################################
    #        E n d    Z a c h a r y     K a r a t e
    ################################################################################################
    ################################################################################################

    ################################################################################################
    ################################################################################################
    #        S a m r a j    N e t w o r k
    ################################################################################################
    ################################################################################################
    
    if to_do == 'samraj_network':
        sn = nx.read_gml('samraj_network.gml').to_undirected()
        sn_components_dict = girvan_newman(sn, print_biggest=False,create_partition=False)
        partition = partition_components_dict(sn,sn_components_dict)
        raise Exception
        sn_ratio_list  = find_big_splits(sn_components_dict)
        # For Zachary's karate the interesting split is the top split '0', which comes second on the ratio list
        (sn_ratio, sn_winner, sn_len1, sn_len2) = sn_ratio_list[1]
        # The Officer cluster only has purity 89.5%, while the Mr. Hi faction has purity 100%
        # There are 2 Mr. Hi nodes tangled up among the others.
        sn_purity = get_cluster_purity(sn,sn_components_dict[sn_winner],'club')
        # Going one level deeper doesnt help. An officer node is split off, not a Mr. Hi node as one might hope.
        sn_purity2 = get_cluster_purity(sn,sn_components_dict[sn_winner+'0'],'club')
        # Going one level further doesnt help either. We get two substantial sub factions,
        # each with one Mr. Hi node.
        sn_purity3 = get_cluster_purity(sn,sn_components_dict[sn_winner+'00'],'club')

    ################################################################################################
    ################################################################################################
    #        E n d    S a m r a j    N e t w o r k
    ################################################################################################
    ################################################################################################




     
