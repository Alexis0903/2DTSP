import numpy as np
from scipy.spatial import KDTree
import argparse
import os

#---------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate an undirected KNN graph.')
parser.add_argument('file', type=str, help='Input file containing points.')
parser.add_argument('output_folder', type=str, default='output', help='Output folder.')
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------------------------------

# Read points
points = {}
with open(args.file, 'r') as f:
    for line in f:
        name, x, y = line.strip().replace('(', '').replace(')', '').replace('-', '').split(';')
        points[name] = (float(x), float(y))

names = list(points.keys())
coords = np.array([points[name] for name in names])

# Choose k based on the number of points
K = max(5,len(names) // 10)

#---------------------------------------------------------------------------------------------------------------------------

# Use KDTree for O(n log n) neighbor queries
tree = KDTree(coords)

# Find k+1 neighbors (to exclude self)
distances, indices = tree.query(coords, k = K + 1)  # Shape: (n, k+1)

# Build undirected edges using sorted tuples to avoid duplicates
edges = set()
for i, (name, neighbors, dist) in enumerate(zip(names, indices, distances)):
    for j, d in zip(neighbors[1:], dist[1:]):
        n1, n2 = sorted([i, j])  # Sort to ensure undirected edge
        edges.add((n1, n2, d))
        
#---------------------------------------------------------------------------------------------------------------------------

# Save to file with unique edge IDs
os.makedirs(args.output_folder, exist_ok=True)
output_file = os.path.join(args.output_folder, os.path.basename(args.file).replace('.txt', '_knn.txt'))
with open(output_file, 'w') as f:
    for idx, (n1, n2, d) in enumerate(sorted(edges), start=1):
        f.write(f"{idx};{names[n1]};{names[n2]};{d}\n")