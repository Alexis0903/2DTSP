import numpy as np
from scipy.spatial import Delaunay
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

parser = argparse.ArgumentParser(description='Generate the Urquhart graph from a set of points.')
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

# Map each edge to its adjacent triangles' third points
edge_to_third = defaultdict(list)
for simplex in tri.simplices:
    sorted_simplex = sorted(simplex)
    for i, j in combinations(sorted_simplex, 2):
        third = [k for k in simplex if k != i and k != j][0]
        edge_to_third[(i, j)].append(third)
        
for key in edge_to_third:
    edge_to_third[key] = sorted(set(edge_to_third[key]))  # Remove duplicates and sort
    
#---------------------------------------------------------------------------------------------------------------------------

# Determine edges to remove (longest in any adjacent triangle)
edges_to_remove = set()
for edge in delaunay_edges:
    i, j = edge
    for third in edge_to_third.get(edge, []):
        # Calculate edge lengths in the triangle
        len_ij = np.linalg.norm(coordinates[i] - coordinates[j])
        len_ik = np.linalg.norm(coordinates[i] - coordinates[third])
        len_jk = np.linalg.norm(coordinates[j] - coordinates[third])
        if len_ij >= max(len_ik, len_jk):
            edges_to_remove.add(edge)
            break  # No need to check other triangles

# Urquhart graph edges
urquhart_edges = [edge for edge in delaunay_edges if edge not in edges_to_remove]

#---------------------------------------------------------------------------------------------------------------------------

# Write output
os.makedirs(args.output_folder, exist_ok=True)
output_file = os.path.basename(args.file).replace('.txt', '_urquhart.txt')
with open(os.path.join(args.output_folder, output_file), 'w') as f:
    for idx, (i, j) in enumerate(urquhart_edges, 1):
        dist = np.linalg.norm(coordinates[i] - coordinates[j])
        f.write(f"{idx};{point_names[i]};{point_names[j]};{dist}\n")