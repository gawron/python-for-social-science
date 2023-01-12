from make_gml_graph import print_gml_graph
edge_dict = dict()
nodes = dict()
num_nodes  = 0

with open('zachary_weighted_matrix.dat','r') as fh:
    for (i,line) in enumerate(fh):
        line = line.strip()
        if line:
            try:
                line_list = [int(e) for e in line.split()]
            except ValueError as e:
                print 'Ill-formed line %d %s' % (i+1,line)
                raise e
            if num_nodes == 0:
                num_nodes = len(line_list)
            assert num_nodes == len(line_list), 'Inconsistent graph, line %d' % (i+1,)
            # wasteful node rep to fit into what print_gml_graph expects.
            nodes[i+1] = dict()
            for (j,weight) in enumerate(line_list):
                if weight > 0:
                    edge_dict[(i+1,j+1)] = weight

print_gml_graph(nodes, edge_dict, 'weighted_karate.gml')
