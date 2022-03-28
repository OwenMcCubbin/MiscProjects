import pymel.core as pm
import random


class ShapesUI():
    
    def __init__(self):
        self.handle = 'TestShapesUI'
        
        if pm.window(self.handle, exists=True):
            pm.deleteUI(self.handle)
            
        ##Comment out the removeal of Prefs before handing it off to client
        if pm.windowPref(self.handle, exists=True):
            pm.windowPref(self.handle, remove=True)
        
        with pm.window(self.handle, title='Shapes', w=300, h=100):
            
            with pm.columnLayout():
                with pm.rowLayout(nc=4):
                    pm.button(l='Sphere', w=100, h=40, command = pm.Callback(self.create_sphere))
                    
                    pm.button(l='Plane', w=100, h=40, command = pm.Callback(self.create_plane))
                    
                    pm.button(l='Random', w=100, h=40, command = pm.Callback(self.create_random))
                    
                    pm.button(l='Random Sphere', w=100, h=40, command = pm.Callback(self.create_random_sphere))
                
                
        pm.showWindow(self.handle)
        
    def create_sphere(self):
        pm.polySphere()
        
    def create_plane(self):
        pm.polyPlane()
        
    def create_random(self):
        ##get random int between 0 and 3 including 3
        rand = random.randrange(0,4)
        ##Use IF statements to create spheres based on the number 
        if rand == 0:
            pm.polyCube()
            
        if rand == 1:
            pm.polyCylinder()
            
        if rand == 2:
            pm.polyCone()
            
        if rand == 3:
            pm.polyTorus()
            
    def create_random_sphere(self):
        ##get random int between 0 and 3 including 3
        rand = random.randint(0,3)
        ##Use IF statements to create spheres based on the number 
        if rand == 0:
            pm.polySphere(r=rand)
            
        if rand == 1:
            pm.polySphere(r=rand)
            
        if rand == 2:
            pm.polySphere(r=rand)
            
        if rand == 3:
            pm.polySphere(r=rand)
        
ShapesUI()