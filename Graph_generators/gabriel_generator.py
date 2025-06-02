import numpy as np
from scipy.spatial import Delaunay, cKDTree
import argparse
import os
from itertools import combinations

#---------------------------------------------------------------------------------------------------------------------------

def get_delaunay_edges(points):
    """Get edges from Delaunay triangulation"""
    tri = Delaunay(points)
    edges = set()
    for simplex in tri.simplices:
        for i, j in combinations(simplex, 2):
            edges.add(tuple(sorted((i, j))))
    return sorted(edges)

#---------------------------------------------------------------------------------------------------------------------------

def is_gabriel_edge(points, i, j, tree):
    """Check if edge (i,j) satisfies Gabriel condition using spatial index"""
    pi, pj = points[i], points[j]
    midpoint = (pi + pj) / 2
    radius = np.linalg.norm(pi - pj) / 2
    
    # Find points within the critical distance
    candidates = tree.query_ball_point(midpoint, radius)
    
    # Exclude endpoints and check emptiness
    return all(k in {i, j} for k in candidates)

#---------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate Gabriel Graph using Delaunay triangulation')
parser.add_argument('file', type=str, help='Input points file')
parser.add_argument('output_folder', type=str, default='output', help='Output directory')
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------------------------------

# Read and parse points
points = {}
with open(args.file, 'r') as f:
    for line in f:
        name, x, y = line.strip().replace('(', '').replace(')', '').replace('-', '').split(';')
        points[name] = (float(x), float(y))

point_names = list(points.keys())
coordinates = np.array(list(points.values()))
n = len(coordinates)

#---------------------------------------------------------------------------------------------------------------------------

# Build spatial index once
tree = cKDTree(coordinates)

# Get candidate edges from Delaunay triangulation
delaunay_edges = get_delaunay_edges(coordinates)

# Check Gabriel condition on Delaunay edges
edges = []
counter = 1

# Use sorted indices to avoid duplicates
for i, j in delaunay_edges:
    if is_gabriel_edge(coordinates, i, j, tree):
        dist = np.linalg.norm(coordinates[i] - coordinates[j])
        edges.append((counter, point_names[i], point_names[j], dist))
        counter += 1
        
#---------------------------------------------------------------------------------------------------------------------------

# Write output
os.makedirs(args.output_folder, exist_ok=True)
output_file = os.path.basename(args.file).replace('.txt', '_gabriel.txt')
with open(os.path.join(args.output_folder, output_file), 'w') as f:
    for edge in edges:
        f.write(f"{edge[0]};{edge[1]};{edge[2]};{edge[3]}\n")