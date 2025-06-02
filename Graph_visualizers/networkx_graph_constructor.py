import networkx as nx

# Function to construct the graph
def construct_graph(nodes, edges):
    
    names = [] 
    for name in nodes.keys() : 
        names.append(name)
    
    # Create a graph using NetworkX
    G = nx.Graph()
    
    # Add nodes with positions
    for name, pos in nodes.items():
        G.add_node(name, pos=pos)

    # Add edges
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if (names[i], names[j]) in edges.keys() or (names[j], names[i]) in edges.keys():
                G.add_edge(names[i], names[j], weight=edges[(names[i], names[j])] if (names[i], names[j]) in edges.keys() else edges[(names[j], names[i])])
    
    return G