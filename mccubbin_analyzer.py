"""
#############################################################################
filename    mccubbin_analyzer.py
author      Owen McCubbin
dP email    owen.mccubbin@digipen.edu
course      CS115/CSX510
Brief Description:
    Basic UI to search for FBX and OBJ objects in a file and create a scene CSV data from them.
    Digipen CS115/CSX510 Spring 2020
    April 3rd 2020
#############################################################################
"""
##import needed packages
import pymel.core as pm
import os
##force a new file to make suere there are no meshes present
pm.newFile(force=True)
##create a class for the analyser UI
class AnalyzerUI():
    ##define self
    def __init__(self):
        ##set up a window handle for the UI
        self.window_handle = 'AnalyzerUI'
        ##check if window already exsists
        if pm.window(self.window_handle, exists = True):
            ##delete it if does exists
            pm.deleteUI(self.window_handle)
        ##Check for window preferences and delete them
        if pm.windowPref(self.window_handle, exists=True):
            pm.windowPref(self.window_handle, remove = True)
            
        ##Determine a size for the window
        with pm.window(self.window_handle, title = 'Scene Analyzer', width = 700, height = 100):
            ##space between collumns
            with pm.columnLayout(rowSpacing = 10):
                ##number of columns
                with pm.rowLayout(numberOfColumns=2):
                    ##Create browse button
                    pm.button(label = 'Browse', width = 100, height = 30, command = pm.Callback(self.browse)) ##Add a callback later once gotten
                    ##create a text feild and make it equal to the file path
                    self.ui_filepath = pm.textField(width=600, height=30)
                
                ##create the go button that will call back a def that opens all files in the directory
                pm.button(label='Go', width = 700, height = 30, command = pm.Callback(self.start_analyze)) ##Add a callback to the command that opens all files in Maya
                
    ##Create the browse def that will allow for file browsing
    def browse(self):
        ##make a variable that is equal to the file search 
        ##file searched for must be a 'file'/directory (fileMode=3)
        result = pm.fileDialog2(dialogStyle=2, fileMode=3, caption='Open')
        
        print (result)
        ## If nothing was selected, do nothing
        if result == None:
            return
        ##set the filepath text to be the directory. 
        self.ui_filepath.setText(result[0])
        
        
    def start_analyze(self):
        ##set the file path for this def
        file_path = self.ui_filepath.getText()
        ##define a path for data to write to
        scene_data = file_path + r"\analysis.csv"
        print scene_data
        ##set a variable for directory
        dir_name = os.path.dirname(scene_data)
        ##if the directory csv doesn't exist, create it
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        with open(scene_data, 'w') as file_handle:
            
            ##Write some column headers to improve readability
            file_handle.write('File Name, Mesh Name, Tri Count, Mesh Area, Mesh Density\n')
        
            ##get all files in the directory and import them
            for file_object in os.listdir(file_path):
                ##make a clear variable for import
                object_file = os.path.join(file_path, file_object)
                print object_file
                ##check that files are obj
                if ".obj" in str(object_file):
                    ##Open/Import file into maya
                    pm.importFile(object_file)
                    ##put all meshes of that file into a list
                    all_mesh_transforms = pm.listTransforms(type='mesh')
                    ##iterate on that list to get info on individual meshes
                    for mesh_transform in all_mesh_transforms:
                        ##get the file name from previous for loop
                        file_name = file_object
                        ##get mesh name
                        mesh_name = mesh_transform.name()
                        ##get tri count
                        tri = mesh_transform.numTriangles()
                        ##get vert count
                        verts = mesh_transform.numVertices()
                        ##get area
                        area = mesh_transform.area()
                        ##use area and tri count to determine density
                        density = float(tri)/area
                        ##output all the data from above into a variable
                        output = '%s, %s, %i, %.2f, %.2f\n' %(file_name, mesh_name, tri, area, density)
                        ##print variable for test
                        print (output)
                        ##use the variable to write in the document
                        file_handle.write(output)
                    ##delete all mesh so that there is a fresh area for the next one. 
                    pm.delete(all_mesh_transforms)
                    
                ##check that files are fbx
                if ".fbx" in str(object_file):
                    ##Open/Import file into maya
                    pm.importFile(object_file)
                    ##iterate on all meshes in file
                    all_mesh_transforms = pm.listTransforms(type='mesh')
                    
                    for mesh_transform in all_mesh_transforms:
                        
                        file_name = file_object
                        
                        mesh_name = mesh_transform.name()
                        
                        tri = mesh_transform.numTriangles()
                        
                        verts = mesh_transform.numVertices()
                        
                        area = mesh_transform.area()
                        
                        density = float(tri)/area
                        
                        output = '%s, %s, %i, %.2f, %.2f\n' %(file_name, mesh_name, tri, area, density)
                        
                        print (output)
                        
                        file_handle.write(output)
                        
                        
                    pm.delete(all_mesh_transforms)
                ##Don't use any file that is not FBX or OBJ
                else:
                    pass
