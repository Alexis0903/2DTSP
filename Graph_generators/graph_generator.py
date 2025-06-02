import subprocess
import os

# Use the generators in the Graphs folder to generate the edges of the graphs
def generate_graphs_edges(selected_graphs, selected_points, python_executable, edges_folder, points_folder):
    
    # The path to the points file is constructed based on the selected points and points folder
    points_file = f"{points_folder}/{selected_points}"
        
    # If the edges folder does not exist, create it
    if not os.path.exists(edges_folder):
        os.makedirs(edges_folder)
        
    #---------------------------------------------------------------------------------------------------------------------------
    
    if "Complete" in selected_graphs:
        
        # This refers to the complete_generator.py script in the Graph_generators folder
        script_path = "Graph_generators/complete_generator.py"
        
        # To run the script, we need:
        # 1. The python executable (python_executable, must be modified in the main notebook)
        # 2. The path to the script (script_path)
        
        # We also need specific arguments:
        # 1. The points file (points_file) : The file containing the points to be used for generating the graph
        # 2. The edges folder (edges_folder) : The folder where the generated edges will be saved
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)
        
    #---------------------------------------------------------------------------------------------------------------------------
    
    if "Delaunay" in selected_graphs:
        
        # This refers to the delaunay_generator.py script in the Graph_generators folder
        script_path = "Graph_generators/delaunay_generator.py"
        
        # To run the script, we need:
        # 1. The python executable (python_executable, must be modified in the main notebook)
        # 2. The path to the script (script_path)
        
        # We also need specific arguments:
        # 1. The points file (points_file) : The file containing the points to be used for generating the graph
        # 2. The edges folder (edges_folder) : The folder where the generated edges will be saved
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)
        
    #---------------------------------------------------------------------------------------------------------------------------
    
    if "Gabriel" in selected_graphs:
        
        # This refers to the gabriel_generator.py script in the Graph_generators folder
        script_path = "Graph_generators/gabriel_generator.py"
        
        # To run the script, we need:
        # 1. The python executable (python_executable, must be modified in the main notebook)
        # 2. The path to the script (script_path)
        
        # We also need specific arguments:
        # 1. The points file (points_file) : The file containing the points to be used for generating the graph
        # 2. The edges folder (edges_folder) : The folder where the generated edges will be saved
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)
        
    #---------------------------------------------------------------------------------------------------------------------------
    
    if "RNG" in selected_graphs:
        
        # This refers to the rng_generator.py script in the Graph_generators folder
        script_path = "Graph_generators/rng_generator.py"
        
        # To run the script, we need:
        # 1. The python executable (python_executable, must be modified in the main notebook)
        # 2. The path to the script (script_path)
        
        # We also need specific arguments:
        # 1. The points file (points_file) : The file containing the points to be used for generating the graph
        # 2. The edges folder (edges_folder) : The folder where the generated edges will be saved
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)
        
    #---------------------------------------------------------------------------------------------------------------------------
        
    if "Urquhart" in selected_graphs:
        
        # This refers to the urquhart_generator.py script in the Graph_generators folder
        script_path = "Graph_generators/urquhart_generator.py"
        
        # To run the script, we need:
        # 1. The python executable (python_executable, must be modified in the main notebook)
        # 2. The path to the script (script_path)
        
        # We also need specific arguments:
        # 1. The points file (points_file) : The file containing the points to be used for generating the graph
        # 2. The edges folder (edges_folder) : The folder where the generated edges will be saved
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)
        
    #---------------------------------------------------------------------------------------------------------------------------
    
    if "d_radius" in selected_graphs:
        
        # This refers to the d_radius_generator.py script in the Graph_generators folder
        script_path = "Graph_generators/d_radius_generator.py"
        
        # To run the script, we need:
        # 1. The python executable (python_executable, must be modified in the main notebook)
        # 2. The path to the script (script_path)
        
        # We also need specific arguments:
        # 1. The points file (points_file) : The file containing the points to be used for generating the graph
        # 2. The edges folder (edges_folder) : The folder where the generated edges will be saved
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)
        
    #---------------------------------------------------------------------------------------------------------------------------
        
    if "KNN" in selected_graphs:
        
        script_path = "Graph_generators/knn_generator.py"
        command = [python_executable, script_path, points_file, edges_folder]
        subprocess.run(command, check=True)