import os

# Once the features are selected, we merge the corresponding files to generate points
def merge_AC_types(selected, output_folder):
    
    # Create the folder to store the points if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Compute the total number of points    
    total = 0
    for choice in selected :
        nb = int(choice.split('[')[1].split(']')[0])
        total += nb
        
    #---------------------------------------------------------------------------------------------------------------------------
        
    with open(f"{output_folder}/AC_{total}.txt", 'w') as file:
        
        for txt_file in os.listdir("AC/AC_database"): # for txt file corresponding to all features...
            
            type = txt_file.split('_')[1].split('.')[0]
            nb = int(txt_file.split('_')[0])
            
            if f"{type} [{nb}]" in selected: # If the feature has been selected...
                
                with open(f"AC/AC_database/{txt_file}", 'r') as txt: # We write it in a common file with other selected features
                    file.write(txt.read())
                    file.write('\n') 