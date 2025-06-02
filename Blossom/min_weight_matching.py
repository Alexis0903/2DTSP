import networkx as nx

from Blossom.max_weight_matching import max_weight_matching

def min_weight_matching(G, graph_name, display,
                        nodes_complete, edges_complete,
                        S_color_code_blossom, T_color_code_blossom,
                        visited_color_code_blossom,
                        matching_color_code_blossom,
                        blossom_color_code_blossom,
                        save_blossom_gif_bool, save_blossom_gif_folder,
                        save_blossom_html_bool, save_blossom_html_folder,
                        weight="weight"):
    
    """Computing a minimum-weight maximal matching of G.

    Use the maximum-weight algorithm with edge weights subtracted
    from the maximum weight of all edges.

    A matching is a subset of edges in which no node occurs more than once.
    The weight of a matching is the sum of the weights of its edges.
    A maximal matching cannot add more edges and still be a matching.
    The cardinality of a matching is the number of matched edges.

    This method replaces the edge weights with 1 plus the maximum edge weight
    minus the original edge weight.

    new_weight = (max_weight + 1) - edge_weight

    then runs :func:`max_weight_matching` with the new weights.
    The max weight matching with these new weights corresponds
    to the min weight matching using the original weights.
    Adding 1 to the max edge weight keeps all edge weights positive
    and as integers if they started as integers.

    You might worry that adding 1 to each weight would make the algorithm
    favor matchings with more edges. But we use the parameter
    `maxcardinality=True` in `max_weight_matching` to ensure that the
    number of edges in the competing matchings are the same and thus
    the optimum does not change due to changes in the number of edges.

    Read the documentation of `max_weight_matching` for more information.

    Parameters
    ----------
    G : NetworkX graph
      Undirected graph

    weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight.
       If key not found, uses 1 as weight.

    Returns
    -------
    matching : set
        A minimal weight matching of the graph.

    See Also
    --------
    max_weight_matching
    """
    
    # Should not happen, but just in case
    if len(G.edges) == 0:
        return max_weight_matching(G, maxcardinality=True, weight=weight)
    
    # It's a list of tuples with the edges and the weight as values
    G_edges = G.edges(data=weight, default=1)
    # Compute the maximum weight
    max_weight = 1 + max(w for _, _, w in G_edges)
    
    # Create a new graph with the new weights
    # The weight is the max_weight plus 1 minus the original weight
    InvG = nx.Graph()
    edges = ((u, v, max_weight - w) for u, v, w in G_edges)
    InvG.add_weighted_edges_from(edges, weight=weight)
    
    # Run the max_weight_matching algorithm with the new weights
    return max_weight_matching(InvG, maxcardinality=True, weight=weight, graph_name = graph_name, display = display,
                               nodes_complete = nodes_complete, edges_complete = edges_complete,
                               S_color_code_blossom = S_color_code_blossom, T_color_code_blossom = T_color_code_blossom,
                               visited_color_code_blossom = visited_color_code_blossom,
                               matching_color_code_blossom = matching_color_code_blossom,
                               blossom_color_code_blossom = blossom_color_code_blossom,
                               save_blossom_gif_bool = save_blossom_gif_bool, save_blossom_gif_folder = save_blossom_gif_folder,
                               save_blossom_html_bool = save_blossom_html_bool, save_blossom_html_folder = save_blossom_html_folder)