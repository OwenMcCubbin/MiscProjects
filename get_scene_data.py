

import pymel.core as pm
import os

# Get all the mesh transform nodes (remember = Pymel works best on the transforms, not the shapes)
all_mesh_transforms = pm.listTransforms(type='mesh') 

# Define a path for the file to be written to
scene_data = r"C:\temp\dp\data.csv"

# Create the directory if it doesn't exist
dir_name = os.path.dirname(scene_data)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Open a file handle using the "with" context
with open(scene_data, 'w') as file_handle:

    # Write some column headers to improve readability in Excel
    file_handle.write('Mesh, Tris, Density\n')
    
    # Loop over all the transforms
    for mesh_transform in all_mesh_transforms:

        # Get the name of the mesh
        name = mesh_transform.name()

        # Get the triangle count of the mesh
        tri = mesh_transform.numTriangles()

        # Get the vertex count of the mesh
        verts = mesh_transform.numVertices()

        # Get the surface area of the mesh
        area = mesh_transform.area()

        # Calculate the triangle density of the mesh
        density = float(tri) / area
        
        # Format the line to write to the file
        output = "%s, %i, %.2f\n" %(name, tri, density)

        # Print to script editor (this is just for feedback / debugging)
        print (output)

        # Write the current line to file
        file_handle.write(output)
        
# When the "with" context exits (here) the file handle will be automatically closed
# You can now open the file in Excel to view the data about the scene
# Sort the columns by selecting the column data (excluding the header) ...
# ... then choose "sort" > "largest to smallest" in the top write (choose to expand selection when asked)
    
    
    