import numpy as np
from scipy.spatial import Delaunay, distance
import argparse
import os
from itertools import combinations
from collections import defaultdict

#---------------------------------------------------------------------------------------------------------------------------

def get_delaunay_edges(tri):
    """Extract unique edges from Delaunay triangulation."""
    edges = set()
    for simplex in tri.simplices:
        for i, j in combinations(simplex, 2):
            edges.add(tuple(sorted((i, j))))
    return sorted(edges)

#---------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate the Relative Neighborhood Graph (RNG) from a set of points.')
parser.add_argument('file', type=str, help='The file containing the points.')
parser.add_argument('output_folder', type=str, default='output', help='The folder where the output file will be saved.')
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------------------------------

# Read points
points = {}
with open(args.file, 'r') as file:
    for line in file:
        parts = line.strip().replace('(', '').replace(')', '').replace('-', '').split(';')
        name, x, y = parts[0], parts[1], parts[2]
        points[name] = (float(x), float(y))

point_names = list(points.keys())
coordinates = np.array(list(points.values()))

#---------------------------------------------------------------------------------------------------------------------------

# Compute Delaunay Triangulation
tri = Delaunay(coordinates)
delaunay_edges = get_delaunay_edges(tri)

#---------------------------------------------------------------------------------------------------------------------------

# Map each edge to its adjacent triangle's third points
edge_to_third = defaultdict(list)
for simplex in tri.simplices:
    sorted_simplex = sorted(simplex)
    for i, j in combinations(sorted_simplex, 2):
        third = [k for k in simplex if k != i and k != j][0]
        edge_to_third[(i, j)].append(third)
        
for key in edge_to_third:
    edge_to_third[key] = sorted(set(edge_to_third[key]))  # Remove duplicates and sort
        
#---------------------------------------------------------------------------------------------------------------------------

# Check RNG condition on Delaunay edges
edges = []
counter = 1
dist_matrix = distance.cdist(coordinates, coordinates, 'euclidean')  # Precompute distances

for i, j in delaunay_edges:
    dij = dist_matrix[i][j]
    is_rng = True
    
    # Check third points from adjacent triangles
    for k in edge_to_third.get((i, j), []):
        if dist_matrix[i][k] < dij and dist_matrix[j][k] < dij:
            is_rng = False
            break
    
    if is_rng:
        edges.append((counter, point_names[i], point_names[j], dij))
        counter += 1
        
#---------------------------------------------------------------------------------------------------------------------------

# Write output
os.makedirs(args.output_folder, exist_ok=True)
output_file = os.path.basename(args.file).replace('.txt', '_rng.txt')
with open(os.path.join(args.output_folder, output_file), 'w') as f:
    for edge in edges:
        f.write(f"{edge[0]};{edge[1]};{edge[2]};{edge[3]}\n")