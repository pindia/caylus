from config import *
from building import *

class Player(object):
    
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.resources = {}
        for resource in RESOURCES:
            self.resources[resource] = 0
        self.resources['food'] = 2
        self.resources['wood'] = 1
        self.resources['money'] = 5
        self.resources['points'] = 0
        self.favors = [-1, -1, -1, -1]
        self.section_batches = [0,0,0]
        
        self.tracks_used = [] # Which favor tracks have been used this phase
        self.when_used = (0,0) # The turn and phase, for purpose of resetting the above
        
    def has_resources(self, resources):
        for resource, amount in resources.items():
            if self.resources[resource] < amount:
                return False
        return True
    
    def add_resources(self, resources):
        for resource, amount in resources.items():
            self.resources[resource] += amount
            
    def remove_resources(self, resources):
        for resource, amount in resources.items():
            self.resources[resource] -= amount
            
    def __str__(self):
        return str(self.resources)
        

            
    def get_money(self):
        return self.resources['money']
    def set_money(self, amt):
        self.resources['money'] = amt    
    money = property(get_money, set_money)
    
    def get_points(self):
        return self.resources['points']
    def set_points(self, amt):
        self.resources['points'] = max(0, amt)
    points = property(get_points, set_points)
    
    @property
    def initial(self):
        return self.name[0].upper()
    

        