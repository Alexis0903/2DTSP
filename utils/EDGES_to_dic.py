# Function to extract the edges from the txt file in the EDGES folder

def retrieve_edges(selected_points, PATH):
    
    path = PATH + '/' + selected_points
        
    with open(path, 'r') as f:
    
        edges = {}
        
        for line in f.readlines():
            
            edge_num, pair_1, pair_2, dist = line.strip().replace('(', '').replace(')', '').split(';')
            pair = (pair_1, pair_2)
            dist = float(dist)
            edges[pair] = dist
            
    return edges