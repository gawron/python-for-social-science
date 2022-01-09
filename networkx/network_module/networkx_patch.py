import networkx as nx

def get_biggest_component (UG):
    components = list(nx.connected_component_subgraphs(UG))
    components.sort(key=lambda x:len(x),reverse=True)
    return components[0]

