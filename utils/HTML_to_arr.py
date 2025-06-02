# Function to extract edges from html files

def retrieve_edges_from_html(selected_points):
    
    with open(selected_points, 'r') as f:
        
        accepted_edges = []
        rejected_edges = []
        
        for line in f.readlines():
            
            if "Accepted" in line:
                edge = line.split('Accepted edge: ')[1].split(' : ')[0].split(' - ')
                accepted_edges.append((edge[0], edge[1]))
                
            if "Rejected" in line:
                edge = line.split('Rejected edge: ')[1].split(' : ')[0].split(' - ')
                rejected_edges.append((edge[0], edge[1]))
                
        return accepted_edges, rejected_edges