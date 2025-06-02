import numpy as np
from scipy.spatial import Delaunay
import itertools
import argparse
import os

#---------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate the Delaunay Triangulation Graph from a set of points.')
parser.add_argument('file', type=str, help='The file containing the points.')
parser.add_argument('output_folder', type=str, default='output', help='The folder where the output file will be saved.')
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------------------------------

# Read points and preprocess
points = {}
with open(args.file, 'r') as f:
    for line in f:
        name, x, y = line.strip().replace('(', '').replace(')', '').replace('-', '').split(';')
        points[name] = (float(x), float(y))

coordinates = np.array(list(points.values()))
point_names = list(points.keys())

#---------------------------------------------------------------------------------------------------------------------------

# Compute Delaunay triangulation (O(n log n))
tri = Delaunay(coordinates)

# Extract unique edges (O(n))
edges_set = set()
for simplex in tri.simplices:
    
    # Iterate over all pairs and ensure each pair is sorted
    for i, j in itertools.combinations(simplex, 2):
        edges_set.add(tuple(sorted((i, j))))
        
#---------------------------------------------------------------------------------------------------------------------------

# Write the edges to the output file
os.makedirs(args.output_folder, exist_ok=True)
output_file = os.path.join(args.output_folder, os.path.basename(args.file).replace('.txt', '_delaunay.txt'))

with open(output_file, 'w') as f:
    for counter, (i, j) in enumerate(edges_set, 1):
        point1, point2 = point_names[i], point_names[j]
        dist = np.linalg.norm(coordinates[i] - coordinates[j])
        f.write(f"{counter};{point1};{point2};{dist}\n")