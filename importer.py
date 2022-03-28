import pymel.core as pm

##Create a class for our importer window
class ImporterUI():
    ##define self
    def __init__(self):
        ##set up a window handle
        self.window_handle = 'ImporterTool' 
        ##check if the windown handle is present, if it is delete it
        if pm.window(self.window_handle, exists=True):
            pm.deleteUI(self.window_handle)
        ##Check if window preferences exist for this tool, if so delete them
        if pm.windowPref(self.window_handle, exists=True):
            pm.windowPref(self.window_handle, remove=True)
        ##Create a window with the handle, give it a title and determine dimensions
        with pm.window(self.window_handle, title='Importer', width=700, height=50):
            ##determine how much space is between columns
            with pm.columnLayout(rowSpacing = 10):
                ##determine the number of columns
                with pm.rowLayout(numberOfColumns=2):
                    ##create a browse button
                    pm.button(label='Browse', width=100, height=30, command=pm.Callback(self.browse))
                    ##create a text field and make it equal to a self variable for later use
                    self.ui_filepath = pm.textField(width=600, height=30)
                    
                pm.button(label='Import', width=700, height=20, command=pm.Callback(self.import_file))
                    
        ##Show the window tool
        pm.showWindow(self.window_handle)
            
            
            
    def browse(self):
        ##fileDialog2 is a file seraching command. fileMode changes the type of files you can search for. Look up help for in depth commands.
        result = pm.fileDialog2(dialogStyle=2, fileMode=1, caption='Import')
        print (result)
        
        if result == None:
            return
        
        self.ui_filepath.setText(result[0])
        
    
    def import_file(self):
        file_path = self.ui_filepath.getText()
        
        pm.importFile(file_path)