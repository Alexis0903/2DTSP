import numpy as np
import pandas as pd

# Function to construct the distance matrix
def construct_distance_matrix(nodes, edges):
    
    names = [] 
    for name in nodes.keys() : 
        names.append(name)

    dists = [[np.inf]*len(nodes) for _ in range(len(nodes))]

    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if (names[i], names[j]) in edges.keys() or (names[j], names[i]) in edges.keys():
                dists[i][j] = dists[j][i] = edges[(names[i], names[j])] if (names[i], names[j]) in edges.keys() else edges[(names[j], names[i])]
                
    dists = np.array(dists)

    #------------------------------------------------------------------------------------------------------------------

    # Create a DataFrame from the distance matrix
    df = pd.DataFrame(dists, columns=names, index=names)
    
    return dists, df