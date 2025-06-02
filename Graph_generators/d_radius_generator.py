import numpy as np
from scipy.spatial import KDTree, distance
import argparse
import os
import math

#---------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate d-radius graph using k-d trees')
parser.add_argument('file', type=str, help='Input file containing points')
parser.add_argument('output_folder', type=str, default='output', help='Output directory')
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------------------------------

# Read and parse points
points = {}
with open(args.file, 'r') as f:
    for line in f:
        # Clean line and split components
        cleaned = line.strip().replace('(', '').replace(')', '').replace('-', '')
        name, x, y = cleaned.split(';')[:3]  # Handle potential trailing semicolons
        points[name] = (float(x), float(y))

point_names = list(points.keys())
coords = np.array([points[name] for name in point_names])
n = len(coords)

#---------------------------------------------------------------------------------------------------------------------------

def mean_distance(coords):
    """Calculate mean distance between all pairs of points."""
    dist_matrix = distance.pdist(coords, 'euclidean')
    mean_dist = np.mean(dist_matrix)
    return mean_dist

#---------------------------------------------------------------------------------------------------------------------------

def max_shortest_distance(points):
    """Finds the maximum of the shortest distances between points"""
    
    def euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    n = len(points)
    if n < 2:
        return 0  # If there's only one point or none, no meaningful distance can be computed
    shortest_distances = []
    
    for i in range(n):
        min_distance = float('inf')
        for j in range(n):
            if i != j:  # Avoid comparing the same point
                distance = euclidean_distance(points[i], points[j])
                min_distance = min(min_distance, distance)
        shortest_distances.append(min_distance)
    
    # Return the maximum among the shortest distances
    return max(shortest_distances)

#---------------------------------------------------------------------------------------------------------------------------

# Define distance threshold here
d = 1.5*mean_distance(coords)  # Mean distance between points

#---------------------------------------------------------------------------------------------------------------------------

# Build KD-tree (O(n log n))
tree = KDTree(coords)

# Find all pairs within distance d (O(n log n + k))
edge_set = set()
results = []
edge_counter = 1

# Batch query for better performance
neighbor_lists = tree.query_ball_tree(tree, d)

# Process neighbors avoiding duplicates
for i in range(n):
    for j in neighbor_lists[i]:
        if i < j:  # Maintain i < j to avoid duplicates
            dist = np.linalg.norm(coords[i] - coords[j])
            edge_set.add((i, j))
            results.append((edge_counter, point_names[i], point_names[j], dist))
            edge_counter += 1
            
#---------------------------------------------------------------------------------------------------------------------------

# Save results
os.makedirs(args.output_folder, exist_ok=True)
output_file = os.path.basename(args.file).replace('.txt', f'_d_radius.txt')
with open(os.path.join(args.output_folder, output_file), 'w') as f:
    for edge in results:
        f.write(f"{edge[0]};{edge[1]};{edge[2]};{edge[3]}\n")