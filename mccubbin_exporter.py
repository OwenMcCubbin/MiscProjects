"""
#######################################
filename    Game Exporter.py
author      Owen McCubbin
dP email    owen.mccubbin@digipen.edu
course      CS115
Brief Description:
    Use this tool to export a mesh with or without LODs and a collision mesh
#######################################
"""
#import needed assets from packages
import pymel.core as pm
import os
#import needed Qt packages
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtUiTools

from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


OV_PREVIOUS_PATH = 'MCCUBBINEXPORTER_PREVIOUS_PATH'
OV_PREVIOUS_NAME = 'MCCUBBINEXPORTER_PREVIOUS_NAME'

def get_maya_window():
    #Return the main Maya window
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def get_script_dir():
    #Returns the directory where the current script lives
    script_file = os.path.abspath(__file__)
    return os.path.dirname(script_file)

#create a new def for the creation of LODs dupes
def create_lod_level(mesh_node, reduction):
    
    #create the new dupe
    lod_dupe = pm.duplicate(mesh_node, rr=True)[0]
    
    #reduce the dupe
    pm.polyReduce(lod_dupe, percentage=reduction)
    
    #returnt he dupe mesh
    return lod_dupe


class ExporterUI(QtWidgets.QDialog):
    
    def __init__(self, parent=get_maya_window()):
        # Run the initialization on the inherited QDialog class
        super(ExporterUI, self).__init__(parent)
        
        # Set the window title
        self.setWindowTitle('Game Exporter')
        
        
        #Osbond Code for helping with Minimize function 
        # Create a flags object from WindowsFlags
        flags = QtCore.Qt.WindowFlags()
        # Assign it to be of type "Dialog" (we are using QWidgets.QDialog above)
        flags = QtCore.Qt.Dialog
        # Add the minimize button using the bitwise operator
        flags |= QtCore.Qt.WindowMinimizeButtonHint
        # If you wanted, this is how to add a maximize (not common for Maya UIs so this is commented out)
        # flags |= QtCore.Qt.WindowMaximizeButtonHint
        # Add a close button, as adding the flags overrides the default close that is there
        flags |= QtCore.Qt.WindowCloseButtonHint
        # Set the flags to the current window object
        self.setWindowFlags(flags)        
        
        
        # Assemble the file path for the ui file
        ui_file_path = os.path.join(get_script_dir(), 'mccubbin_exporter.ui')
        
        # Creat a QFile object form the file path
        qfile_object = QtCore.QFile(ui_file_path)
        
        # Open the QFile object
        qfile_object.open(QtCore.QFile.ReadOnly)
        
        # Create a QUI Loader
        loader = QtUiTools.QUiLoader()
        
        # Load the file as save it to a property
        self.ui = loader.load(qfile_object, parentWidget=self)
        
        #button calls
        #call for the target directroy button
        self.ui.btnTarget.clicked.connect(self.target)
        
        #call for the export button
        self.ui.btnExport.clicked.connect(self.export)
        
        #Testing Combo box stuff
        #adding all needed items to combo box
        self.ui.cmbType.addItem(".ma")
        self.ui.cmbType.addItem(".mb")
        self.ui.cmbType.addItem(".fbx")
        self.ui.cmbType.addItem(".obj")
        
        # Close the file handle
        qfile_object.close()
        
        # Show the UI
        self.show()
        
        #set up the previous path stored data
        previous_path = pm.optionVar.get(OV_PREVIOUS_PATH, "")
        self.ui.linePath.setText(previous_path)
        
        #set up the previous name stored data
        previous_name = pm.optionVar.get(OV_PREVIOUS_NAME, "")
        self.ui.lineName.setText(previous_name)
    
    #Create a def to update the path for target directroy
    def target(self):
        #set the result to be able to be a new file/file that doesn't exist
        #take care to use fileDialog2, don't forget the 2
        results = pm.fileDialog2(fileMode=2)
        #if no path or file was chosen, just return 
        if results is None:
            return
        
        """update the target directory for the next time exported"""
        #update the text path in the window
        self.ui.linePath.setText(results[0])
        #update the previous path
        pm.optionVar[OV_PREVIOUS_PATH] = results[0]
        
    def export(self):
        
        #store the current scene path for later
        scene_path = pm.sceneName()
        print('Scene Path = ', scene_path)
        if scene_path == None or scene_path =='':
            pm.warning('Scene not saved')
            return
        ##save scene before doing stuff
        pm.saveFile()
        
        #grab taget path
        target_path = self.ui.linePath.text()
        #grab file name from the editable line text
        file_name = self.ui.lineName.text()
        
        """update the file name and keep it stored for reopening"""
        #update the text path in the window
        self.ui.lineName.setText(file_name)
        #update the previous path
        pm.optionVar[OV_PREVIOUS_NAME] = file_name
        
        #create a new file path from target and file_name
        new_file = target_path + r'/' + file_name
        print(new_file)
        
        #group all meshes
        all_meshes = pm.listTransforms(type='mesh')
        
        #create a variable for LOD_count
        lod_count = self.ui.sldLODCount.value()
        
        #debug/test print
        #print (lod_count)
        
        #create variable for LOD percent
        lod_percent = self.ui.sldLODPercent.value()
        
        #create a variable for Collision percent
        collision_percent = self.ui.sldCollisionPercent.value()
        
        #itterate on all the meshes
        for each_mesh in all_meshes:
            #check if the collision check box is checked
            if self.ui.chkCollision.isChecked() == True:
                #print tests
                print('Collision True')
                
                #duplicate each mesh
                collision_name = each_mesh.name() + '_collision'
                
                #create duplicate
                collision_dupe = pm.duplicate(each_mesh, name = collision_name)[0]
                
                #create reduction percent variable
                collision_reduction = self.ui.sldCollisionPercent.value()
                
                #reduce by amount
                pm.polyReduce(collision_dupe, percentage=collision_reduction)
                
            else:
                print('Collision False')
                pass
            
            #check if LODs are wanted
            if self.ui.chkLOD.isChecked() == True:
                #debug print to make sure
                print ('LOD True')
                
                #create a new variable for the value in the slider
                num_of_lods = self.ui.sldLODCount.value()
                
                #create a new varaible for the LOD percentage 
                lod_percent = self.ui.sldLODPercent.value()
                
                #create a new variable for the original mesh
                current_mesh = each_mesh
                
                #create a list for the LODs to be put into 
                lod_levels = [current_mesh]
                
                #iterate on the mesh from 0 to the number in the ui
                for i in xrange(0, num_of_lods):
                    
                    #call the lod_level def from earlier and continually update the current mesh varaible
                    current_mesh = create_lod_level(current_mesh, lod_percent)
                    
                    #add the dupe to the list
                    lod_levels.append(current_mesh)
                
                #select the list for creating into a LOD group
                pm.select(lod_levels)
                
                #creat the LOD group
                pm.mel.LevelOfDetailGroup()
                
                
            else:
                print ('LOD False')
                pass
            
            
        #notify the user that no LODs or Collisions will be made when exported with these settings
        if self.ui.chkCollision.isChecked() == False and self.ui.chkLOD.isChecked() == False:
            pm.warning('No LODs or collision meshes created, continuing to export')
            return
        
        #print the current integer of the combo box
        print (self.ui.cmbType.currentIndex())
        #export in the file format needed
        extension = self.ui.cmbType.currentText()
        export_file = new_file + extension
        pm.exportAll(export_file, force=True)
        
        pm.openFile(scene_path, force=True)
        
def run():
    #check to see if the QT widget already exists
    for ui_item in QtWidgets.qApp.allWidgets():
        #If the QT item matches the one in this script than close it
        if type(ui_item).__name__ == 'ExporterUI':
            #Close file
            ui_item.close()
            
    ExporterUI()
    