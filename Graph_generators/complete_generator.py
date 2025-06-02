import math
import argparse
import os
import itertools

#---------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate the Complete Graph from a set of points.')

parser.add_argument('file', type=str, help='The file containing the points.')
parser.add_argument('output_folder', type=str, default='output', help='The folder where the output file will be saved.')

args = parser.parse_args()

points_file = args.file
output_folder = args.output_folder

#---------------------------------------------------------------------------------------------------------------------------

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#---------------------------------------------------------------------------------------------------------------------------

# Read points from the file
points = {}
with open(points_file, 'r') as file:
    for line in file:
        name, x, y = line.strip().replace('(', '').replace(')', '').replace('-', '').split(';')
        x, y = map(float, (x, y))
        points[name] = (x, y)
        
#---------------------------------------------------------------------------------------------------------------------------

# Generate unique edges using combinations to avoid duplicates
edges = []
counter = 1

# Iterate over all unique pairs of points
for (name1, point1), (name2, point2) in itertools.combinations(points.items(), 2):
    
    # Sort the pair of names to ensure alphabetical order
    name1, name2 = sorted([name1, name2])
    
    distance = calculate_distance(point1, point2)
    edges.append((counter, name1, name2, distance))
    counter += 1
    
#---------------------------------------------------------------------------------------------------------------------------

# Create output filename and ensure output folder exists
output_file = os.path.basename(points_file).replace('.txt', '_complete.txt')
os.makedirs(output_folder, exist_ok=True)
os.chmod(output_folder, 0o777)

# Write edges to file
with open(os.path.join(output_folder, output_file), 'w') as file:
    for edge in edges:
        file.write(f"{edge[0]};{edge[1]};{edge[2]};{edge[3]}\n")