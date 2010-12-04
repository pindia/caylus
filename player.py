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
        
    def pretty_resources(self):
        out = ''
        for resource in RESOURCES:
            out += resource[0].upper() * self.resources[resource]
            if out[-1] != ' ':
                out += ' '
        return out
            
    def get_money(self):
        return self.resources['money']
    def set_money(self, amt):
        self.resources['money'] = amt    
    money = property(get_money, set_money)
    
    def get_points(self):
        return self.resources['points']
    def set_points(self, amt):
        self.resources['points'] = amt    
    points = property(get_points, set_points)
    
    
    
class TextPlayer(Player):
    def make_decision(self, decision):
        if isinstance(decision, WorkerDecision):
            print '%s Placing worker. Workers:%d Money:%d' % (self.name, self.workers, self.money)
            print self.pretty_resources()
            for i, building in enumerate(decision.buildings):
                print '%d: %s' % (i, building)
            i = int(raw_input('Your decision:'))
            self.game.make_decision(decision, i)
        elif isinstance(decision, ActionDecision):
            print '%s taking action' % (self.name)
            for i, action in enumerate(decision.actions):
                print '%d: %s' % (i, action)
            i = int(raw_input('Your decision:'))
            self.game.make_decision(decision, i)
        