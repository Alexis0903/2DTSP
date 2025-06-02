# Function to extract the nodes from the txt file in the POINTS folder

def retrieve_nodes(selected_points, PATH):
    
    path = PATH + '/' + selected_points
    
    with open(path, 'r') as f:

        nodes = {}
        
        for line in f.readlines():
            
            name, x, y = line.strip().replace('(', '').replace(')', '').replace('-', '').split(';')
            location = (x, y)
            
            if "AC" not in selected_points:
                location = (float(location[0]), -1 * float(location[1]))  # -1 because the ref is the top left corner
                
            location = (float(location[0]), float(location[1]))
            nodes[name] = location
            
    # for key in nodes:
    #     print(key, nodes[key])
        
    return nodes