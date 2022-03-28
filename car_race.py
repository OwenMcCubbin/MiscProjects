import random
import pymel.core as pm

class Car():
    def __init__(self, make, model):
        self.make = make
        self.model = model
        
        self.distance = 0.0
        
    def update(self):
        self.distance += random.uniform(3,10)
        print (self.make, ('-'*int(self.distance)))
        if self.distance >= 100:
            print (self.make, 'is the winner')

car_1 = Car('Nissan', 'GT-R')
car_2 = Car('Jaguar', 'F-Type')
car_3 = Car('Porsche', '911')
print (car_1.distance)     
while car_1.distance < 100 and car_2.distance < 100 and car_3.distance < 100:
    car_1.update()
    car_2.update()
    car_3.update()