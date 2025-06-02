import os
from Graph_visualizers.graph_plot import plot_graph

def edges_intersect(p1, p2, p3, p4):
    
    # ccw is for counter-clockwise check
    # The idea is to check if two points are on opposite sides of the line formed by the other two points
    # If they are, then the segments intersect
    def ccw(a, b, c):
        return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

#=============================================================================================================

def optimize_tour(points, base_nodes, base_edges, display, graph_name,
                  nodes_complete, edges_complete, shortcutting_edges_color_code,
                  crossing_edges_color_code, corrected_edges_color_code,
                  save_two_opt_html, save_two_opt_html_folder,
                  save_two_opt_gif, save_two_opt_gif_folder):
    
    # Precompute node names lookup
    node_names = {tuple(v): k for k, v in nodes_complete.items()}
    
    #--------------------------------------------------------------------------------------------------------------
    
    # Initialize the HTML content to see which edges are accepted and which are rejected if required
    if save_two_opt_html == True:
    
        # The css style and the beginning of the body + the colors
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>2-opt Visualization</title>
            <style>
                .A {{ color: {shortcutting_edges_color_code}; }}
                .R {{ color: {crossing_edges_color_code}; }}
            </style>
        </head>
        '''
        
        # Add the title
        html_content +=  f'''
        <body>
            <h1>2-opt Visualization for {graph_name}</h1>
            <ul>
        '''

    #--------------------------------------------------------------------------------------------------------------
    
    n = len(points)
    improved = True
    
    temp = points.copy() + [points[0]]  # Circular tour helper
    
    images = []         # To store the images for the gif
    count = 1           # To keep track of the number of steps done

    while improved:
        improved = False
        title = None
        
        # Generate all non-adjacent edge pairs once per iteration
        pairs = [(i, (i + k) % n) for i in range(n) for k in range(2, n-1)]
        
        #-------------------------------------------------------------------------------------------------------------
        
        # Use pairwise checking with optimized indices
        for i, j in pairs:
            a, b = temp[i], temp[i+1]
            c, d = temp[j], temp[j+1]
            
            #-------------------------------------------------------------------------------------------------------------

            if edges_intersect(a, b, c, d):
                
                # Node name lookups (for visualization)
                node_a = node_names[tuple(a)]
                node_b = node_names[tuple(b)]
                node_c = node_names[tuple(c)]
                node_d = node_names[tuple(d)]
                
                # Show the edges in the title
                title = f"Step {count} - Intersecting Edges: ({node_a} - {node_b}) and ({node_c} - {node_d})"
                
                #--------------------------------------------------------------------------------------------------------------

                # If we want to save the html content, we add the edge to the html content
                if save_two_opt_html == True:
                    html_content += f'<li class="A">Step {count} - Intersecting Edges: ({node_a} - {node_b}) and ({node_c} - {node_d})</li>'

                #--------------------------------------------------------------------------------------------------------------
                
                # Perform 2-opt swap
                if j > i:
                    temp[i+1:j+1] = temp[j:i:-1]
                else:
                    segment = (temp[i+1:] + temp[:j+1])[::-1]
                    split = len(temp) - (i + 1)
                    temp[i+1:] = segment[:split]
                    temp[:j+1] = segment[split:]
                        
                #-------------------------------------------------------------------------------------------------------------
            
                # Save the gif of the kruskal algorithm step by step if required   
                if save_two_opt_gif == True:
                    
                    # Display the edges of the shortcutted tour
                    edges_to_display = [[]]
                    for i in range(len(temp)-1):
                        node_1 = next((k for k, v in nodes_complete.items() if v == temp[i]), None)
                        node_2 = next((k for k, v in nodes_complete.items() if v == temp[i+1]), None)
                        edges_to_display[0].append((node_1, node_2))
                    
                    # Display the crossing edges
                    # Display the corrected edges
                    
                    edges_to_display.append([(node_a, node_b), (node_c, node_d)])
                    edges_to_display.append([(node_a, node_c), (node_b, node_d)])
                    
                    colors_edges_to_display = [shortcutting_edges_color_code, crossing_edges_color_code, corrected_edges_color_code]
                    label_edges_to_display = ["Shortcutted Tour", "Crossing Edges", "Corrected Edges"]
                    
                    # what we provide here is for 1 frame !!!    
                    img = plot_graph(base_nodes=base_nodes, base_edges=base_edges, display=display,
                                    complete_nodes=nodes_complete, complete_edges=edges_complete,
                                    plot_name=title, upper_folder=save_two_opt_gif_folder,
                                    add_edges_to_display=edges_to_display, colors_add_edges_to_display=colors_edges_to_display, label_add_edges_to_display=label_edges_to_display,
                                    add_nodes_to_display=None, colors_add_nodes_to_display=None, label_add_nodes_to_display=None,
                                    gif_bool=True)
                    
                    images.append(img)
                    
                count += 1  # Increment the step count
                    
                #-------------------------------------------------------------------------------------------------------------

                # Update working structures
                points[:] = temp[:-1]
                temp = points.copy() + [points[0]]
                improved = True
                count += 1
                
            #-------------------------------------------------------------------------------------------------------------
            else:
                
                # Find nodes name corresponding to the positions
                node_a = next((k for k, v in nodes_complete.items() if v == a), None)
                node_b = next((k for k, v in nodes_complete.items() if v == b), None)
                node_c = next((k for k, v in nodes_complete.items() if v == c), None)
                node_d = next((k for k, v in nodes_complete.items() if v == d), None)
                
                # Show the edges in the title
                title = f"Step {count} - Non-Intersecting Edges: ({node_a} - {node_b}) and ({node_c} - {node_d})"
                
                # If we want to save the html content, we add the edge to the html content
                if save_two_opt_html == True:
                    html_content += f'<li class="R">Step {count} - Non-Intersecting Edges: ({node_a} - {node_b}) and ({node_c} - {node_d})</li>'
                    
                count += 1  # Increment the step count
                    
            #-------------------------------------------------------------------------------------------------------------

            if improved:
                break  # Exit i loop to restart search

    #-------------------------------------------------------------------------------------------------------------
    # If we want to save the html content, we close the html content
    if save_two_opt_html == True:    
        
        html_content += '''
            </ul>
        </body>
        </html>
        '''
        
        # Save the html content in the save_two_opt_html_folder
        if not os.path.exists(save_two_opt_html_folder):
            os.makedirs(save_two_opt_html_folder)
        
        with open(f"{save_two_opt_html_folder}/{graph_name}.html", 'w') as f:
            f.write(html_content)
            
    #-------------------------------------------------------------------------------------------------------------
    
    # If we want to save the gif of the kruskal algorithm step by step...
    if save_two_opt_gif == True:
        
        if not os.path.exists(save_two_opt_gif_folder):
            os.makedirs(save_two_opt_gif_folder)
            
        # Save all frames as a GIF in the save_two_opt_gif_folder
        if images:
            
            images[0].save(
                f'{save_two_opt_gif_folder}/{graph_name}.gif',
                save_all=True,
                append_images=images[1:],
                duration=1000, # Milliseconds per frame
                loop=0,        # Loop forever
                optimize=True  # Reduce file size
            )

    return points