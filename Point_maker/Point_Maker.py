# import 
import cv2
import tkinter as tk
from tkinter.simpledialog import askstring
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Point Maker')

parser.add_argument('map_name', type=str, default='Map.JPG', help='The name of the map to load')
parser.add_argument('output_folder', type=str, default='.', help='The folder where to save the output file')

args = parser.parse_args()

map_name = args.map_name
output_folder = args.output_folder

#================================================================================================

# Function to update the image with last infos
#--------------------------------------------------------------------------------------------------------

def update_display():

    '''
    The aim of this is to update the image size.
    '''

    #--------------------------------------------------------------------------------------------------------
    
    global actual_image # The actual image with the previously added points in red
    global current_zoom, x_offset, y_offset # The zoom parameters
    global zoomed_image
    
    #--------------------------------------------------------------------------------------------------------

    # We zoom on the original image 
    zoomed_image = cv2.resize(actual_image.copy(), None, fx=current_zoom, fy=current_zoom, interpolation=cv2.INTER_LINEAR)

    #--------------------------------------------------------------------------------------------------------
    
    # Calculate the maximum allowable offsets to avoid going out of bounds (the program crahses and return an error in this case)
    max_x_offset = max(zoomed_image.shape[1] - actual_image.shape[1], 0)
    max_y_offset = max(zoomed_image.shape[0] - actual_image.shape[0], 0)

    #--------------------------------------------------------------------------------------------------------
    
    # Limit x_offset and y_offset to stay within bounds
    x_offset = max(0, min(x_offset, max_x_offset))
    y_offset = max(0, min(y_offset, max_y_offset))

    #--------------------------------------------------------------------------------------------------------
    
    # Apply offsets to simulate movement
    zoomed_image = zoomed_image[y_offset:y_offset + actual_image.shape[0], x_offset:x_offset + actual_image.shape[1]]
    
#================================================================================================

# Functions to zoom in the image 
#------------------------------------------------------------------------------------------------------------------

def zoom_in():
    
    '''
    This is a function to zoom in the map. 
    '''
    
    global current_zoom, zoom_factor # The zoom parameters
    global zoomed_image
    
    current_zoom *= zoom_factor # Updates the currrent zoom
    
    update_display() # Updates the window of the actual image
    
    # Displays what has been done to this point 
    cv2.imshow('Image', zoomed_image)
    
#------------------------------------------------------------------------------------------------------------------

def zoom_out():
    
    '''
    This is a function to zoom out the map. 
    '''
    
    global current_zoom, zoom_factor # The zoom parameters
    global zoomed_image
    
    current_zoom /= zoom_factor # Updates the currrent zoom
    
    update_display() # Updates the window of the actual image
    
    # Displays what has been done to this point 
    cv2.imshow('Image', zoomed_image)
    
#================================================================================================

# Function to move on the zoomed map
#------------------------------------------------------------------------------------------------------------------

def move(direction):
    
    '''
    This is a function to move on the zoomed map.
    '''
    
    global x_offset, y_offset, move_step # The movement parameters
    global zoomed_image
    
    #------------------------------------------------------------------------------------------------------------------
    # To move up on the zoomed map
    if direction == 'up':
        y_offset -= move_step
        
    #------------------------------------------------------------------------------------------------------------------
    # To move down on the zoomed map   
    elif direction == 'down':
        y_offset += move_step
        
    #------------------------------------------------------------------------------------------------------------------
    # To move left on the zoomed map    
    elif direction == 'left':
        x_offset -= move_step
        
    #------------------------------------------------------------------------------------------------------------------
    # To move right on the zoomed map   
    elif direction == 'right':
        x_offset += move_step
        
    #------------------------------------------------------------------------------------------------------------------
        
    update_display()
    
    # Displays what has been done to this point 
    cv2.imshow('Image', zoomed_image)
    
#================================================================================================

# Function to add a point
#--------------------------------------------------------------------------------------------------------

def add_point(event, x, y, flags, param):

    '''
    The aim of this function is to add a point on the loaded image. The added point will be a node and should be an interest point on the map.

    Arg :
    event : An action defined in cv2. Here it is the right click to add a point. 
    x,y : The position of the point in the current window (as we allow zoom).
    flags,param : not used, mandatory to use this function
    
    '''
    global actual_image # The actual image with the previously added points in red
    global final # The final image with all ever added points
    
    global all_points # The dictionnary of all ever added points
    
    global x_offset, y_offset, current_zoom # The zoom parameters
    
    global zoomed_image

    # When the right click is pressed 
    if event == cv2.EVENT_RBUTTONDOWN:

        #--------------------------------------------------------------------------------------------------------

        # Store the point in the original image coordinates (as we're working on a zommed window)
        original_x = int((x + x_offset) / current_zoom)
        original_y = int((y + y_offset) / current_zoom)

        #--------------------------------------------------------------------------------------------------------
        
        # Create a Tkinter root window (hidden). Mean window of the program
        root = tk.Tk()
        root.withdraw()

        #--------------------------------------------------------------------------------------------------------
        
        # Display an input dialog to enter the name for the point
        point_name = askstring("Point Name", "Enter a name for the point:")

        #--------------------------------------------------------------------------------------------------------
        
        # Check if a name was entered
        if point_name:
            
            # We add a red circle at pointed point on the actual image
            cv2.circle(actual_image, (original_x, original_y), 5, (0, 0, 255), -1)
            
            # We add a blue circle at pointed point on the final image
            cv2.circle(final, (original_x, original_y), 5, (255, 0, 0), -1)
            
            # Store the point and its coordinates in the dictionaries of the names
            all_points[point_name] = (original_x,original_y)

        #--------------------------------------------------------------------------------------------------------
        
        # We replace the previous version of the images with the new one with our new point
        cv2.imwrite('Map_with_red_points.JPG', actual_image)
        cv2.imwrite('Map_with_blue_points.JPG', final)

        # Destroy the root window
        root.destroy()

        #--------------------------------------------------------------------------------------------------------

        # Update the image using our function defined above
        update_display()
        
        # Displays what has been done to this point 
        cv2.imshow('Image', zoomed_image)
        
#================================================================================================

# Mean part of the code to add points 
#------------------------------------------------------------------------------------------------------------------

# We define a dict that will contain all ever added points and their position
all_points = {}

#------------------------------------------------------------------------------------------------------------------

# We load the original image and make a copy of it on which we'll add points 
original_image = cv2.imread(map_name)

# Create a copy of the original that we will update with temporary red points
temporary = original_image.copy()
cv2.imwrite('Map_with_red_points.JPG', temporary)

# Create a copy of the original that we will update with all ever added blue points
final = original_image.copy()
cv2.imwrite('Map_with_blue_points.JPG', final)

#------------------------------------------------------------------------------------------------------------------

boo = True
while boo :  

    #------------------------------------------------------------------------------------------------------------------

    # Zoom parameters
    zoom_factor = 1.2  # You can adjust the zoom factor
    current_zoom = 1.0 # Must be initialized at 1 

    # Movement parameters
    x_offset = 0 # Must be initialized at 0
    y_offset = 0 # Must be initialized at 0
    
    move_step = 30 # You can adjust the movement factor

    #------------------------------------------------------------------------------------------------------------------

    # Load your JPEG image
    actual_image = cv2.imread('Map_with_blue_points.JPG')

    #------------------------------------------------------------------------------------------------------------------

    # Create a window and set the mouse callback function
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', add_point)

    #------------------------------------------------------------------------------------------------------------------
    
    # Displays what has been done to this point 
    cv2.imshow('Image', actual_image)

    while True:        

        #------------------------------------------------------------------------------------------------------------------

        # Wait for user to add points and press a key
        key = cv2.waitKey(1) & 0xFF

        if key == ord('p'): # You finished part of the points
            break
        
        elif key == ord('+'): # To zoom in 
            zoom_in()
            
        elif key == ord('-'): # To zoom out
            zoom_out()
            
        elif key == ord('w') : # To move down
            move('down')
            
        elif key ==  ord('z'): # To move up
            move('up')
            
        elif key == ord('q') : # To move left
            move('left')
            
        elif key ==  ord('s'): # To move right
            move('right')

        elif key == ord('y'): # You finished adding all your points
            boo = False 
            break 

    #------------------------------------------------------------------------------------------------------------------

    cv2.destroyAllWindows()

#------------------------------------------------------------------------------------------------------------------

# Print all points with their names
# for name, location in all_points.items():
#     print(f"Name: {name}, Location: {location}")

#------------------------------------------------------------------------------------------------------------------
# And write them in an external file 

# Specify the name of the output text file
output_file = map_name.split('.')[0].split('/')[-1] + '_' + str(len(all_points)) + '.txt'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    os.chmod(output_folder, 0o777)

# Open the file in write mode to write all names
with open(output_folder + '/' + output_file, "w") as file:
    for name, location in all_points.items():
        file.write(str(name) + ';' + '(' + str(location[0]) + ';' + str(location[1]) + ')' + '\n')