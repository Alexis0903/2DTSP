from networkx.utils import arbitrary_element
from Graph_visualizers.graph_plot import plot_graph
import os

# Inspired by https://networkx.org/documentation/stable/_modules/networkx/algorithms/euler.html#eulerian_circuit

def eulerian_circuit(G_sup, source_node, display,
                     graph_edges, graph_name,
                     nodes_complete, edges_complete,
                     accepted_edges_color_code,
                     rejected_edges_color_code,
                     save_eulerian_circuit_gif, save_eulerian_circuit_gif_folder,
                     save_eulerian_circuit_html, save_eulerian_circuit_html_folder):
    
    """Hierholzer's algorithm with shortest-neighbor prioritization"""
    
    # Create a working copy of the graph
    G = G_sup.copy()
    
    # To save the edges that are accepted and rejected
    EDGES_A = []
    EDGES_R = []
    
    # The stack of vertices that we are traversing, starting with the source node    
    vertex_stack = [source_node]
    last_vertex = None
    
    # Save the images for the GIF
    images = []
    
    #-------------------------------------------------------------------------------------------------------------
    
    # Initialize the HTML content to see which edges are accepted and which are rejected if required
    if save_eulerian_circuit_html == True:
    
        # The css style and the beginning of the body + the colors
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Hierholzer Visualization</title>
            <style>
                .A {{ color: {accepted_edges_color_code}; }}
                .R {{ color: {rejected_edges_color_code}; }}
            </style>
        </head>
        '''
        
        # Add the title
        html_content +=  f'''
        <body>
            <h1>Hierholzer Visualization for {graph_name}</h1>
            <ul>
        '''
        
    #-------------------------------------------------------------------------------------------------------------
    
    count = 0
    while vertex_stack:
        
        # The current vertex is the last vertex in the stack
        count += 1
        current_vertex = vertex_stack[-1]
        
        #-------------------------------------------------------------------------------------------------------------
        
        if G.degree(current_vertex) == 0:
            
            # Add to circuit if we have a connecting edge
            if last_vertex is not None:
                EDGES_A.append((last_vertex, current_vertex))
                
                #-------------------------------------------------------------------------------------------------------------
            
                # If we want to save the GIF...
                if save_eulerian_circuit_gif == True:
                
                    # Display the accepted edges and the rejected edges
                    # Some edges were rejected and then became accepted
                    edges_to_display = [EDGES_A,
                                        [edge for edge in EDGES_R if (edge not in set(EDGES_A) and (edge[1], edge[0]) not in set(EDGES_A))]]
                    colors_edges_to_display = [accepted_edges_color_code, rejected_edges_color_code]
                    label_edges_to_display = ['accepted', 'rejected']
                    
                    # Display the current vertex in red
                    nodes_to_display = [[current_vertex]]
                    colors_nodes_to_display = ['red']
                    label_nodes_to_display = ['current']
                    
                    # The title of the plot with the weights of the edges
                    title = f"Step {count} - Accepted edge: {last_vertex} - {current_vertex} : {edges_complete[(last_vertex, current_vertex)] if (last_vertex, current_vertex) in edges_complete else edges_complete[(current_vertex, last_vertex)]}"
                    
                    # what we provide here is for 1 frame !!!    
                    img = plot_graph(base_nodes=nodes_complete, base_edges=graph_edges,display=display,
                                     complete_edges=edges_complete, complete_nodes=nodes_complete,
                                     plot_name=title, upper_folder=save_eulerian_circuit_gif_folder,
                                     add_edges_to_display=edges_to_display,colors_add_edges_to_display=colors_edges_to_display, label_add_edges_to_display=label_edges_to_display,
                                     add_nodes_to_display=nodes_to_display, colors_add_nodes_to_display=colors_nodes_to_display, label_add_nodes_to_display=label_nodes_to_display,
                                     gif_bool=True)   
                    
                    images.append(img)
                    
                #-------------------------------------------------------------------------------------------------------------
                
                # If we want to save the HTML content...
                if save_eulerian_circuit_html == True:
                    html_content += f'<li class="A">Step {count} - Accepted edge: {last_vertex} - {current_vertex} : {edges_complete[(last_vertex, current_vertex)] if (last_vertex, current_vertex) in edges_complete else edges_complete[(current_vertex, last_vertex)]}</li>\n'
                
                #-----------------------------------------------------------------------------------------------
                
            # We update the last vertex and remove the current vertex from the stack
            last_vertex = current_vertex
            vertex_stack.pop()
            
        #-------------------------------------------------------------------------------------------------------------
        # We're here in the first time we have to accept an edge
        
        else:
            
            # _, next_vertex = arbitrary_element(edges(current_vertex))
            
            # Define the next vertex to visit as the closest one to the current vertex
            next_vertex = sorted(G.edges(current_vertex), key=lambda x: edges_complete[x] if x in edges_complete else edges_complete[(x[1], x[0])])[0][1]
            
            # Add the edge between the current vertex and the next vertex to the rejected edges
            EDGES_R.append((current_vertex, next_vertex))
            
            #-------------------------------------------------------------------------------------------------------------
            
            # If we want to save the GIF...
            if save_eulerian_circuit_gif == True:
                
                # Display the accepted edges and the rejected edges
                # Some edges were rejected and then became accepted
                edges_to_display = [EDGES_A,
                                    [edge for edge in EDGES_R if (edge not in set(EDGES_A) and (edge[1], edge[0]) not in set(EDGES_A))]]
                
                colors_edges_to_display = [accepted_edges_color_code, rejected_edges_color_code]
                label_edges_to_display = ['accepted', 'rejected']
                
                # Display the current vertex in red
                nodes_to_display = [[current_vertex]]
                colors_nodes_to_display = ['red']
                label_nodes_to_display = ['current']
                
                # The title of the plot with the weights of the edges
                title = f"Step {count} - Rejected edge: {current_vertex} - {next_vertex} : {edges_complete[(current_vertex, next_vertex)] if (current_vertex, next_vertex) in edges_complete else edges_complete[(next_vertex, current_vertex)]}"
                
                # what we provide here is for 1 frame !!!    
                img = plot_graph(base_nodes=nodes_complete, base_edges=graph_edges,display=display,
                                 complete_edges=edges_complete, complete_nodes=nodes_complete,
                                 plot_name=title, upper_folder=save_eulerian_circuit_gif_folder,
                                 add_edges_to_display=edges_to_display,colors_add_edges_to_display=colors_edges_to_display, label_add_edges_to_display=label_edges_to_display,
                                 add_nodes_to_display=nodes_to_display, colors_add_nodes_to_display=colors_nodes_to_display, label_add_nodes_to_display=label_nodes_to_display,
                                 gif_bool=True)
                
                images.append(img)
                
            #-------------------------------------------------------------------------------------------------------------
            
            # If we want to save the HTML content...
            if save_eulerian_circuit_html == True:
                html_content += f'<li class="R">Step {count} - Rejected edge: {current_vertex} - {next_vertex} : {edges_complete[(current_vertex, next_vertex)] if (current_vertex, next_vertex) in edges_complete else edges_complete[(next_vertex, current_vertex)]}</li>\n'
            
            #-------------------------------------------------------------------------------------------------------------
            
            # Update the stack and remove the edge between the current vertex and the next vertex
            vertex_stack.append(next_vertex)
            G.remove_edge(current_vertex, next_vertex)
            
    #-------------------------------------------------------------------------------------------------------------
    
    # Add the very last edge between the source node (last vertex in the stack) and the node starting the circuit (if they're different)
    if EDGES_A[0][0] != source_node:
        
        EDGES_A.append((source_node, EDGES_A[0][0]))
        count += 1
        
        if save_eulerian_circuit_gif == True:
            
            # Display the accepted edges and the rejected edges
            # Some edges were rejected and then became accepted
            edges_to_display = [EDGES_A,
                                [edge for edge in EDGES_R if (edge not in set(EDGES_A) and (edge[1], edge[0]) not in set(EDGES_A))]]
            
            colors_edges_to_display = [accepted_edges_color_code, rejected_edges_color_code]
            label_edges_to_display = ['accepted', 'rejected']
            
            # Display the current vertex in red
            nodes_to_display = [[EDGES_A[0][0]]]
            colors_nodes_to_display = ['red']
            label_nodes_to_display = ['current']
            
            # The title of the plot with the weights of the edges
            title = f"Step {count} - Accepted edge: {source_node} - {EDGES_A[0][0]} : {edges_complete[(source_node, EDGES_A[0][0])] if (source_node, EDGES_A[0][0]) in edges_complete else edges_complete[(EDGES_A[0][0], source_node)]}"
            
            # what we provide here is for 1 frame !!!    
            img = plot_graph(base_nodes=nodes_complete, base_edges=graph_edges,display=display,
                             complete_edges=edges_complete, complete_nodes=nodes_complete,
                             plot_name=title, upper_folder=save_eulerian_circuit_gif_folder,
                             add_edges_to_display=edges_to_display,colors_add_edges_to_display=colors_edges_to_display, label_add_edges_to_display=label_edges_to_display,
                             add_nodes_to_display=nodes_to_display, colors_add_nodes_to_display=colors_nodes_to_display, label_add_nodes_to_display=label_nodes_to_display,
                             gif_bool=True)
            
            images.append(img)
            
        #-------------------------------------------------------------------------------------------------------------
        
        # If we want to save the HTML content...
        if save_eulerian_circuit_html == True:
            html_content += f'<li class="A">Step {count} - Accepted edge: {source_node} - {EDGES_A[0][0]} : {edges_complete[(source_node, EDGES_A[0][0])] if (source_node, EDGES_A[0][0]) in edges_complete else edges_complete[(EDGES_A[0][0], source_node)]}</li>\n'
            
    #-------------------------------------------------------------------------------------------------------------
    
    # If we want to save the GIF...        
    if save_eulerian_circuit_gif == True:        
        
      if not os.path.exists(save_eulerian_circuit_gif_folder):
         os.makedirs(save_eulerian_circuit_gif_folder)
         
      # Save all frames as a GIF in the save_eulerian_circuit_gif_folder
      if images:
         
         images[0].save(
               f'{save_eulerian_circuit_gif_folder}/{graph_name}_eulerian_circuit.gif',
               save_all=True,
               append_images=images[1:],
               duration=1000, # Milliseconds per frame
               loop=0,        # Loop forever
               optimize=True  # Reduce file size
         )
         
    #-------------------------------------------------------------------------------------------------------------
    
    # If we want to save the html content, we close the html content
    if save_eulerian_circuit_html == True:
        
        html_content += '''
            </ul>
        </body>
        </html>
        '''
        
        # Save the html content in the save_eulerian_circuit_html_folder
        if not os.path.exists(save_eulerian_circuit_html_folder):
            os.makedirs(save_eulerian_circuit_html_folder)
        
        with open(f"{save_eulerian_circuit_html_folder}/{graph_name}.html", 'w') as f:
            f.write(html_content)
            
    #-------------------------------------------------------------------------------------------------------------
    
    # The eulerian circuit is the list of accepted edges        
    return EDGES_A