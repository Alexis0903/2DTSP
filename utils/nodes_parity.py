# Function to establish the parity of the degrees of the nodes based on the edges

def establish_parity_degree(edges):
    
    degrees = {}
    
    for edge in edges:
        if edge[0] in degrees:
            degrees[edge[0]] += 1
        else:
            degrees[edge[0]] = 1
        if edge[1] in degrees:
            degrees[edge[1]] += 1
        else:
            degrees[edge[1]] = 1
            
    return degrees

# degrees = establish_parity_degree(accepted_edges)
# for key in degrees:
#     print(key, degrees[key])

# odd_degrees = {key: value for key, value in degrees.items() if value % 2 != 0}
# print(odd_degrees)