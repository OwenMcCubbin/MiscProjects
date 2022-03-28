import random

class Player():
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.ammo = 10
        
    def shoot(self):
        shots_fired = random.randint(1,4)
        if shots_fired > self.ammo:
            shots_fired = self.ammo
        self.ammo -= shots_fired
        return shots_fired
        
    def get_hit(self,shots):
        impact = random.randint(0, shots)
        self.health -= (impact * 8)
        if self.health <= 0:
            print self.name, 'is dead'
            
    def collect(self):
        chance = random.uniform(0,1)
        if chance > 0.7:
            new_ammo = random.randint(0,8)
            self.ammo += new_ammo
        
    def attack(self, target):
        shots = self.shoot()
        target.get_hit(shots)
        self.collect()
        
        print self.name, 'Health', ('+' * self.health)
        print self.name, 'Ammo', ('^' * self.ammo)
        
    
        
player_1 = Player("Kai")
player_2 = Player("Grif")

for i in xrange(0,100):
    if player_1.health > 0 and player_2.health > 0:
        player_1.attack(player_2)
        player_2.attack(player_1)