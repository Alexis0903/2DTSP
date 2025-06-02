from Graph_visualizers.graph_plot import plot_graph
import os

def shortcutting(circuit, display,
                 base_nodes, base_edges,
                 nodes_complete, edges_complete,
                 graph_name,
                 accepted_edges_color_code,
                 rejected_edges_color_code,
                 save_shortcutting_gif, save_shortcutting_gif_folder,
                 save_shortcutting_html, save_shortcutting_html_folder):
    
    nodes = []
    images = []
    count = 1
    
    #-----------------------------------------------------------------------------------------------------------------------
    
    # If we want to save the shortcutting html...
    if save_shortcutting_html == True:
        
        # The css style and the beginning of the body + the colors
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Shortcutting Visualization</title>
            <style>
                .A {{ color: {accepted_edges_color_code}; }}
                .R {{ color: {rejected_edges_color_code}; }}
            </style>
        </head>
        '''
        
        # Add the title
        html_content +=  f'''
        <body>
            <h1>Shortcutting Visualization for {graph_name}</h1>
            <ul>
        '''
    
    #-----------------------------------------------------------------------------------------------------------------------
    
    # For every edge in the circuit...
    for u, v in circuit:
        
        # If nodes is empty, we are in the very beginning of the circuit
        # We add the node u to the list of nodes
        if not nodes:
            nodes.append(u)
            
        #-----------------------------------------------------------------------------------------------------------------------
        
        # If the node v is already in the list of nodes, we go to the next edge
        if v in nodes:
            
            #-----------------------------------------------------------------------------------------------------------------------
            
            # If we want to save the shortcutting gif...
            if save_shortcutting_gif == True:
                
                # The edges to display are the edges of the circuit, and the rejected edge (u, v)
                edges_to_display = [[(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)],
                                    [(u, v) if (u,v) in edges_complete else (v, u)]]
                colors_edges_to_display = [accepted_edges_color_code, rejected_edges_color_code]
                label_edges_to_display = ['Shortcutted tour', 'Rejected edge']
                
                # If we're in the very first step, we may have u == v, so we put 0
                if u == v:
                    title = f"Step {count} - Rejected edge: {u} - {v} : 0<li>\n"
                else:
                    title = f"Step {count} - Rejected edge: {u} - {v} : {edges_complete[(u, v)] if (u, v) in edges_complete else edges_complete[(v, u)]}"
                
                # Display the current vertex in red
                nodes_to_display = [[u]]
                colors_nodes_to_display = ['red']
                label_nodes_to_display = ['current']
                    
                img = plot_graph(base_nodes=base_nodes, base_edges=base_edges, display=display,
                           complete_nodes=nodes_complete, complete_edges=edges_complete,
                           plot_name=title, upper_folder=save_shortcutting_gif_folder,
                           add_edges_to_display=edges_to_display, colors_add_edges_to_display=colors_edges_to_display, label_add_edges_to_display=label_edges_to_display,
                           add_nodes_to_display=nodes_to_display, colors_add_nodes_to_display=colors_nodes_to_display, label_add_nodes_to_display=label_nodes_to_display,
                           gif_bool=True)
                
                images.append(img)
                
            #-----------------------------------------------------------------------------------------------------------------------
            
            # If we want to save the shortcutting html...
            if save_shortcutting_html == True:
                
                # Add the edge to the html content
                # If we're in the very first step, we may have u == v, so we put 0
                if u == v:
                    html_content += f'<li class="R">Step {count} - Rejected edge: {u} - {v} : 0</li>\n'
                else:
                    html_content += f'<li class="R">Step {count} - Rejected edge: {u} - {v} : {edges_complete[(u, v)] if (u, v) in edges_complete else edges_complete[(v, u)]}</li>\n'
            
            count += 1
            
            # We go to the next edge and skip the rest of the loop
            continue
        
        #-------------------------------------------------------------------------------------------------------------------------
            
        # If we reached this point, the edge (u, v) is accepted     
        # We add the node v to the list of nodes
        nodes.append(v)
        
        #-----------------------------------------------------------------------------------------------------------------------
        
        # If we want to save the shortcutting gif...
        if save_shortcutting_gif == True:
            
            # The edges to display are the edges of the circuit, and the accepted edge (u, v)
            edges_to_display = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
            
            title = f"Step {count} - Accepted edge: {u} - {v} : {edges_complete[(u, v)] if (u, v) in edges_complete else edges_complete[(v, u)]}"
            
            # Display the current vertex in red
            nodes_to_display = [[u]]
            colors_nodes_to_display = ['red']
            label_nodes_to_display = ['current']
                
            img = plot_graph(base_nodes=base_nodes, base_edges=base_edges, display=display,
                       complete_nodes=nodes_complete, complete_edges=edges_complete,
                       plot_name=title, upper_folder=save_shortcutting_gif_folder,
                       add_edges_to_display=[edges_to_display], colors_add_edges_to_display=[accepted_edges_color_code], label_add_edges_to_display=['Shortcutted tour'],
                       add_nodes_to_display=nodes_to_display, colors_add_nodes_to_display=colors_nodes_to_display, label_add_nodes_to_display=label_nodes_to_display,
                       gif_bool=True)
            
            images.append(img)
            
        #-----------------------------------------------------------------------------------------------------------------------
        
        # If we want to save the shortcutting html...
        if save_shortcutting_html == True:
            
            # Add the edge to the html content
            html_content += f'<li class="A">Step {count} - Accepted edge: {u} - {v} : {edges_complete[(u, v)] if (u, v) in edges_complete else edges_complete[(v, u)]}</li>\n'
            
        count += 1
    
    #------------------------------------------------------------------------------------------------------------------------
    
    # Finish the cycle with the first node    
    nodes.append(nodes[0])
    
    #-----------------------------------------------------------------------------------------------------------------------
    
    # If we want to save the shortcutting gif...
    if save_shortcutting_gif == True:
        
        # The edges to display are the edges of the circuit, and the accepted edge (nodes[-2], nodes[0])
        edges_to_display = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
        
        title = f"Step {count} - Accepted edge: {nodes[-2]} - {nodes[0]} : {edges_complete[(nodes[-2], nodes[0]) if (nodes[-2], nodes[0]) in edges_complete else (nodes[0], nodes[-2])]}"
        
        # Display the current vertex in red
        nodes_to_display = [[u]]
        colors_nodes_to_display = ['red']
        label_nodes_to_display = ['current']
                
        img = plot_graph(base_nodes=base_nodes, base_edges=base_edges, display=display,
                     complete_nodes=nodes_complete, complete_edges=edges_complete,
                     plot_name=title, upper_folder=save_shortcutting_gif_folder,
                     add_edges_to_display=[edges_to_display], colors_add_edges_to_display=[accepted_edges_color_code], label_add_edges_to_display=['Shortcutted tour'],
                     add_nodes_to_display=nodes_to_display, colors_add_nodes_to_display=colors_nodes_to_display, label_add_nodes_to_display=label_nodes_to_display,
                     gif_bool=True)
        
        images.append(img)
        
    #-----------------------------------------------------------------------------------------------------------------------
    
    # If we want to save the shortcutting html...
    if save_shortcutting_html == True:
        
        # Add the edge to the html content
        html_content += f'<li class="A">Step {count} - Accepted edge: {nodes[-2]} - {nodes[0]} : {edges_complete[(nodes[-2], nodes[0])] if (nodes[-2], nodes[0]) in edges_complete else edges_complete[(nodes[0], nodes[-2])]}</li>\n'
        
        # Finish the html content
        html_content += '''
            </ul>
        </body>
        </html>
        '''
        
        # Save the html content in the save_kruskal_html_folder
        if not os.path.exists(save_shortcutting_html_folder):
            os.makedirs(save_shortcutting_html_folder)
            
        with open(f'{save_shortcutting_html_folder}/{graph_name}.html', 'w') as file:
            file.write(html_content)
    #-----------------------------------------------------------------------------------------------------------------------
    
    # If we want to save the gif of the shortcutting...
    if save_shortcutting_gif == True:
        
        if not os.path.exists(save_shortcutting_gif_folder):
            os.makedirs(save_shortcutting_gif_folder)
            
        # Save all frames as a GIF in the save_kruskal_gif_folder
        if images:
            
            images[0].save(
                f'{save_shortcutting_gif_folder}/{graph_name}.gif',
                save_all=True,
                append_images=images[1:],
                duration=1000, # Milliseconds per frame
                loop=0,        # Loop forever
                optimize=True  # Reduce file size
            )
            
    #-----------------------------------------------------------------------------------------------------------------------
    
    return nodes