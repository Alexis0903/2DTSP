import os

from Graph_visualizers.graph_plot import plot_graph
from Kruskal.UnionFind import UnionFind

# Inspired by https://www.thepingouin.com/2024/10/15/implementer-lalgorithme-de-kruskal-en-python-pour-trouver-un-arbre-couvreur-minimal/

# Function to run the kruskal algorithm step by step
def kruskal_stepwise(G, reversed_mapping, display,
                     base_nodes, base_edges,
                     nodes_complete, edges_complete,
                     graph_name,
                     accepted_edges_color_code,
                     rejected_edges_color_code,
                     save_kruskal_gif, save_kruskal_gif_folder,
                     save_kruskal_MST, save_kruskal_MST_folder,
                     save_kruskal_html, save_kruskal_html_folder):
    
    # Sort the edges by weight and initialize the UnionFind data structure
    edges = sorted(G.edges(data=True), key=lambda e: e[2]['weight'])
    uf = UnionFind(len(G.nodes))
    accepted, rejected = [], []
    
    #-------------------------------------------------------------------------------------------------------------
    
    # Initialize the HTML content to see which edges are accepted and which are rejected if required
    if save_kruskal_html == True:
    
        # The css style and the beginning of the body + the colors
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Kruskal Visualization</title>
            <style>
                .A {{ color: {accepted_edges_color_code}; }}
                .R {{ color: {rejected_edges_color_code}; }}
            </style>
        </head>
        '''
        
        # Add the title
        html_content +=  f'''
        <body>
            <h1>Kruskal Visualization for {graph_name}</h1>
            <ul>
        '''
    
    #-------------------------------------------------------------------------------------------------------------
    
    images = []         # To store the images for the gif
    count = 1           # To keep track of the number of steps done
    total_weight = 0    # To store the total weight of the MST
    
    for u, v, data in edges:
        
        title = None
        
        # Stop when MST is complete
        if len(accepted) == len(G.nodes) - 1:
            break
        
        #-------------------------------------------------------------------------------------------------------------
        
        # If including this edge doesn't cause cycle, then include it in result
        if uf.union(u, v):
            
            # Add the edge to the MST (with the original node names)
            accepted.append((reversed_mapping[u], reversed_mapping[v]))
            
            # Show the edge in the title
            title = f"Step {count} - Accepted edge: {reversed_mapping[u]} - {reversed_mapping[v]} : {data['weight']}"
            
            # If we want to save the html content, we add the edge to the html content
            if save_kruskal_html == True:
                html_content += f'<li class="A">Step {count} - Accepted edge: {reversed_mapping[u]} - {reversed_mapping[v]} : {data["weight"]}</li>\n'
            
            # Increment the number of steps done
            count += 1
            
            # Increment the total weight of the MST
            total_weight += data['weight']
            
        #-------------------------------------------------------------------------------------------------------------
        
        # Else discard the edge    
        else:
            
            # Add the edge to the rejected edges (with the original node names)
            rejected.append((reversed_mapping[u], reversed_mapping[v]))
            
            # Show the edge in the title
            title = f"Step {count} - Rejected edge: {reversed_mapping[u]} - {reversed_mapping[v]} : {data['weight']}"
            
            # If we want to save the html content, we add the edge to the html content
            if save_kruskal_html == True:
                html_content += f'<li class="R">Step {count} - Rejected edge: {reversed_mapping[u]} - {reversed_mapping[v]} : {data["weight"]}</li>\n'
            
            # Increment the number of steps done
            count += 1
            
        #-------------------------------------------------------------------------------------------------------------
        
        # Save the gif of the kruskal algorithm step by step if required   
        if save_kruskal_gif == True:
            
            # Display the accepted and rejected edges
            edges_to_display = [accepted, rejected]
            colors_edges_to_display = [accepted_edges_color_code, rejected_edges_color_code]
            label_edges_to_display = ['accepted', 'rejected']
            
            # The base nodes and edges are the ones provided in the arguments
            # The title of the frame is the title we defined above
            # The additonal edges to display are the accepted and rejected edges
            
            # what we provide here is for 1 frame !!!    
            img = plot_graph(base_nodes=base_nodes, base_edges=base_edges, display=display,
                             complete_nodes=nodes_complete, complete_edges=edges_complete,
                             plot_name=title, upper_folder=save_kruskal_gif_folder,
                             add_edges_to_display=edges_to_display, colors_add_edges_to_display=colors_edges_to_display, label_add_edges_to_display=label_edges_to_display,
                             add_nodes_to_display=None, colors_add_nodes_to_display=None, label_add_nodes_to_display=None,
                             gif_bool=True)
            
            images.append(img)
        
    #-------------------------------------------------------------------------------------------------------------
    
    # If we want to save the html content, we close the html content
    if save_kruskal_html == True:    
        
        html_content += '''
            </ul>
        </body>
        </html>
        '''
        
        # Save the html content in the save_kruskal_html_folder
        if not os.path.exists(save_kruskal_html_folder):
            os.makedirs(save_kruskal_html_folder)
        
        with open(f"{save_kruskal_html_folder}/{graph_name}.html", 'w') as f:
            f.write(html_content)
    
    #-------------------------------------------------------------------------------------------------------------
    
    # If we want to save the gif of the kruskal algorithm step by step...
    if save_kruskal_gif == True:
        
        if not os.path.exists(save_kruskal_gif_folder):
            os.makedirs(save_kruskal_gif_folder)
            
        # Save all frames as a GIF in the save_kruskal_gif_folder
        if images:
            
            images[0].save(
                f'{save_kruskal_gif_folder}/{graph_name}.gif',
                save_all=True,
                append_images=images[1:],
                duration=1000, # Milliseconds per frame
                loop=0,        # Loop forever
                optimize=True  # Reduce file size
            )
        
    #-------------------------------------------------------------------------------------------------------------
    
    # If we want to save the final MST...
    if save_kruskal_MST == True:
            
        # Save the final MST in the save_kruskal_MST_folder
        if not os.path.exists(save_kruskal_MST_folder):
            os.makedirs(save_kruskal_MST_folder)
           
        # The total weight of the MST is displayed in the title
        # The accepted edges are displayed in accepted_edges_color_code
            
        plot_graph(base_nodes=base_nodes, base_edges=base_edges, display=display,
                   complete_nodes=nodes_complete, complete_edges=edges_complete,
                   plot_name=f"MST for {graph_name} : {total_weight} (total weight)", upper_folder=save_kruskal_MST_folder,
                   add_edges_to_display=[accepted], colors_add_edges_to_display=[accepted_edges_color_code], label_add_edges_to_display=['MST'],
                   add_nodes_to_display=None, colors_add_nodes_to_display=None, label_add_nodes_to_display=None,
                   gif_bool=False)
        
    return accepted, rejected