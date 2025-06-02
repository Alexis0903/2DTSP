import os
import networkx as nx
import matplotlib.pyplot as plt
import io
from PIL import Image

from Graph_visualizers.networkx_graph_constructor import construct_graph

# Function to plot the graph based on the nodes and edges dictionaries
def plot_graph(base_nodes, base_edges, complete_nodes, complete_edges, 
               display = {'node_size': 50, 'node_color': 'skyblue', 'edge_color': 'lightgray', 'font_size': 2},
               plot_name = None, upper_folder = None,
               add_edges_to_display = None, colors_add_edges_to_display = None, label_add_edges_to_display = None,
               add_nodes_to_display = None, colors_add_nodes_to_display = None, label_add_nodes_to_display = None,
               gif_bool = None):

        
    #------------------------------------------------------------------------------------------------------------------

    # Initialize the plot
    fig = plt.figure(figsize=(20, 20))
    plt.title(plot_name, fontsize=30)
    
    # Construct the graph based on the nodes and edges dictionaries
    G = construct_graph(base_nodes, base_edges)
    G_complete = construct_graph(complete_nodes, complete_edges)
    
    #------------------------------------------------------------------------------------------------------------------
    
    # Get the node positions of the graph based on the placement of nodes in the complete graph
    node_positions = {}
    for node in G.nodes():
        node_positions[node] = G_complete.nodes[node]['pos']
    position = nx.spring_layout(G, pos=node_positions, fixed=node_positions.keys())

    # Create dictionaries for node and edge labels
    node_labels = {node: node for node in G.nodes()}
        
    #------------------------------------------------------------------------------------------------------------------
    
    # Draw the initial graph with nodes in skyblue and edges in light gray
    nx.draw_networkx(
        G,
        pos=position,
        with_labels=False,
        width=1,
        node_color=display['node_color'],
        node_size=display['node_size'],
        edge_color=display['edge_color'],
    )
    
    # Adds the nodes labels
    nx.draw_networkx_labels(G, pos=position, labels=node_labels, font_size=display['font_size'], font_color='black')
    
    #------------------------------------------------------------------------------------------------------------------
    
    # If add_nodes_to_display is not None, we display the sets of nodes mentioned in the list
    if add_nodes_to_display is not None:
        for i in range(len(add_nodes_to_display)): # For every set of nodes to display...
            
            # Update the node positions of the nodes to display
            for node in add_nodes_to_display[i]:
                node_positions[node] = G_complete.nodes[node]['pos']
            position = nx.spring_layout(G, pos=node_positions, fixed=node_positions.keys())
            
            nx.draw_networkx_nodes(G, position,
                                   nodelist=add_nodes_to_display[i],
                                   node_color=colors_add_nodes_to_display[i],
                                   label=label_add_nodes_to_display[i],
                                   node_size=display['node_size']*1.5)
    
    #------------------------------------------------------------------------------------------------------------------
    
    # If add_edges_to_display is not None, we display the sets of edges mentioned in the list
    if add_edges_to_display is not None:
        for i in range(len(add_edges_to_display)):
            
            nx.draw_networkx_edges(G, position,
                                   edgelist=add_edges_to_display[i],
                                   edge_color=colors_add_edges_to_display[i],
                                   label=label_add_edges_to_display[i],
                                   width=2)

    #------------------------------------------------------------------------------------------------------------------
    
    
    # Add a legend to the plot if there is one
    if add_edges_to_display is not None or add_nodes_to_display is not None:
        plt.legend()
    
    if gif_bool == True:
        
        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300)  # Adjust DPI for quality/size
        plt.close(fig)  # Close the figure to free memory
        buf.seek(0)
        
        # Convert buffer to PIL Image and optimize
        img = Image.open(buf)
        return img
    
    #------------------------------------------------------------------------------------------------------------------
    
    else:
        
        # If the upper folder does not exist, we create it
        if not os.path.exists(upper_folder):
            os.makedirs(upper_folder)
            
        # Check if there are additional informations in the title
        if ' : ' in plot_name:
            plot_name = plot_name.split(' :')[0]
            
        # Save the plot
        plt.savefig(upper_folder + '/' + plot_name + '.pdf')
        plt.close()