"""
Code for outputting graphs in graphml format.

All of the following is implemented following the informal
spec given in::

http://graphml.graphdrawing.org/primer/graphml-primer.html

Graphs INPUT to this code are assumed to be in the following format::

    --- C{nodes}: a list of NODE DESCRIPTION DICTIONARIES, each representing a node
    in our graph. Each dictionary MUST have the key C{name}, but may also have other
    keys representing other arbitrary info about the entity being represented by the
    node (eg. gender, address, location, and so on).  Node names must be unique.
    
    --- C{weight_dict}:  a dict of the form::
    
        -- C{source} -> C{Counter}

    X{source} is a string which is the name (C{n['name']}) for some node C{n} in
    C{nodes}.  
    
    C{Counter} is a multiset representation.  The multiset is a dictionary which for
    each key string C{target} returns an C{int}, which represents
    the weight of the edge from C{source} to C{target} in the
    graph.  Hence, X{target} must be the name (C{n['name']}) for some node C{n} in
    C{nodes}.  

    Thus an edge is uniquely identified by a pair of strings, C{(source, target)}, 
    and C{weight_dict[source][target]} returns the edge weight.

Currently supported node attributes (keys to be found in a node description dictionary)::
    -- name
    -- label
    -- color

Supported edge attributes::
   -- weight

NYI extensions.  We may represent arbitrary edge attributes with an additional
dictionary C{edge_dict} whose keys are pairs of C{(source,target)} strings,
and whose values are edge description dictionaries.

   
"""

def print_graphml_graph_to_file (graphfile, nodelist, weight_dict, **options):
    with open(graphfile,'w') as ofh:
        print >> ofh, build_graph(nodelist,weight_dict,**options)

def build_graph (nodelist, weight_dict, **options):
    """
    C{weight_dict} is a dict of the form:
        -- C{source} -> C{Counter}
    X{source} is a string, a name.
    
    C{Counter} is a multiset, essentially a dict which for
    each key string C{target} returns an C{int}, which will be used
    as the weight for an edge from C{source} to C{target} in the
    graph.

    From the list C{nodes}, we make a first make a list of dictionaries
    adding any attributes we want nodes to have (e.g., color).
    In a later implementation we pass in a list of dicts.
    """
    (graph_nodes_str,id_dict) = make_nodes(nodelist, **options)
    graph_edges_str = make_edges(id_dict, weight_dict)
    return assemble_graph (graph_nodes_str, graph_edges_str)

def make_nodes (nodelist, **options):
    """
    Each C{n} is list C{nodelist} must a dict withh at
    least the key C{name}.

    C{options} is a key value dict oof graphj options.
    Currently onlt the default color for a node is supported.

    Return a string giving the node specs for the graphml graph.
    """
    global nodes, id_dict
    
    (nodes,id_dict,ctr,id_template) = ([],{}, 0, "n%d")
    default_color = options.get('default_color',"yellow")
    
    for n in nodelist:
        id_str = id_template % (ctr,)
        ctr += 1
        (name,id_num) = (n['name'],n['id_num'])
        try:
            label = n['label']
            this_node_str = labelled_node_str
        except KeyError:
            label = None
            this_node_str = node_str
        id_dict[(name,id_num)] = id_str
        color = n.get('color',default_color)
        nodes.append(this_node_str % (id_str, name, color))

    return ('\n'.join(nodes),id_dict)


def assemble_graph(graph_nodes_str,graph_edges_str):
    graph_body = graph_wrapper % (graph_nodes_str, graph_edges_str)
    return graph_xml_str % (att_decs, graph_body)


def make_edges(id_dict, weight_dict):
    """
    Currently the only attribute an edge can have is weight, represented
    in C{weight_dict}::
       -- weight_dict[source][target] -> weight ( an integer )
       
    """
    global edgelist,e_dict
    e_dict = weight_dict
    edgelist = []
    for (s, s_targets) in weight_dict.iteritems():
        for (t, tct) in s_targets.iteritems():
            edgelist.append(edge_str % (id_dict[s],id_dict[t],tct))
    return '\n'.join(edgelist)


####################################################
###  Core Graph Wrapper
#####################################################

## args: node decs. edge decs
graph_wrapper = \
"""
<graph id="G" edgedefault="directed">
  %s
  %s
  </graph>
"""

####################################################
###  Edge/Node Attribute Wrapper
###  Part of graphml header declarations
#####################################################

### XML attribute keys for name,color, weight,
att_decs = \
"""
<key id="d0" for="node" attr.name="name" attr.type="string"/>
<key id="d1" for="node" attr.name="color" attr.type="string">
    <default>black</default>
  </key>
<key id="d2" for="edge" attr.name="weight" attr.type="double"/>
"""

####################################################
###  Node Wrapper
#####################################################

# Args: node id, name, color
# we distinguish node id from name
node_str = \
"""
<node id="%s">
<data key = "d0">%s</data>
<data key = "d1">%s</data>
</node>
"""

####################################################
###  Edge Wrapper
#####################################################

# Args: src, tgt, weight
edge_str = \
"""
<edge source="%s" target="%s">
<data key="d2">%.1f</data>
</edge>
"""


#####################################################
##  XML Metainfo Wrapper
#####################################################

## Args  key decs, graph body
graph_xml_str = """\
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns 
     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
%s
%s
</graphml>
"""
