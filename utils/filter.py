import collections

def eliminate_duplicate_edges(file_path):
    edges = []

    with open(file_path, 'r') as f:  # Open the file in read mode
        lines = f.readlines()        # Read all lines into a list

    count = 1
    with open(file_path, 'w') as f:  # Open the file in write mode
        
        for line in lines:
            
            # Split the line into its components
            number, pt1, pt2, dist = line.strip().split(';')

            # Check if the edge is unique
            if (pt1, pt2) not in edges and (pt2, pt1) not in edges:
                edges.append((pt1, pt2))  # Add the edge to the list
                f.write(f'{count};{pt1};{pt2};{dist}\n')
                count += 1
                
#===========================================================================================================================

# def duplicate_odd_degrees_edges(file_path):
    
#     # Read the edges from the file
#     edges = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             parts = line.strip().split(';')
#             if len(parts) == 4:
#                 edges.append((parts[1], parts[2], float(parts[3])))

#     # Create a degree count for each node
#     degree_count = collections.defaultdict(int)
#     for src, dst, _ in edges:
#         degree_count[src] += 1
#         degree_count[dst] += 1

#     # Identify nodes with degree 1
#     leaf_nodes = {node for node, degree in degree_count.items() if degree == 1}

#     # Duplicate edges for leaf nodes in reverse order
#     duplicated_edges = edges.copy()
#     for src, dst, weight in edges:
#         if dst in leaf_nodes:
#             duplicated_edges.append((dst, src, weight))
#         if src in leaf_nodes:
#             duplicated_edges.append((src, dst, weight))

#     # Write the updated list of edges to the file
#     with open(file_path, 'w') as file:
#         for i, (src, dst, weight) in enumerate(duplicated_edges, start=1):
#             file.write(f'{i};{src};{dst};{weight}\n')