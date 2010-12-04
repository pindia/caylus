from config import *



class Action(object):
    def can_execute(self, player):
        return True
    
    def execute(self, player):
        raise Exception('Not implented')

class NullAction(Action):
    def execute(self, player):
        pass
    
    def __repr__(self):
        return '(None)'
        
        
class MoveProvostAction(Action):
    def __init__(self, spaces):
        self.spaces = spaces
        
    def can_execute(self, player):
        return 0 < player.game.provost + self.spaces < LAST_SPACE
        
    def execute(self, player):
        player.game.provost += self.spaces
        
    def __repr__(self):
        return 'P%+d' % self.spaces
       
class ProduceAction(Action):
    def __init__(self, **output):
        self.output = output
        
    def execute(self, player):
        player.add_resources(self.output)
        
    def __repr__(self):
        return format_resources(self.output)
        
class TradeAction(Action):
    ''' An action that involves exchanging some amount of resources/money for others.'''
    def __init__(self, input, output={}):
        self.input = input
        self.output = output
        
    def can_execute(self, player):
        return player.has_resources(self.input)
        
    def execute(self, player):
        player.remove_resources(self.input)
        player.add_resources(self.output)
        
    def __repr__(self):
        return '%s->%s' % (format_resources(self.input), format_resources(self.output))
        
class JoustAction(TradeAction):
    def __init__(self):
        TradeAction.__init__(self, input={'cloth':1, 'money':1}, output={})
        
    def execute(self, player):
        player.remove_resources(self.input)
        game.award_favor(player)
        
    def __repr__(self):
        return '%s->RF' % format_resources(self.input)
        
class ConstructAction(TradeAction):
    def __init__(self, building, cost):
        self.building = building
        TradeAction.__init__(self, input=cost, output={})
        
    def can_execute(self, player):
        # Prevent double construction of buildings
        return TradeAction.can_execute(self, player) and self.building in player.game.wood_buildings
        
    def execute(self, player):
        player.remove_resources(self.input)
        if self.building in player.game.wood_buildings:
            player.game.wood_buildings.remove(self.building)
        if null_building in player.game.normal_buildings:
            player.game.normal_buildings[player.game.normal_buildings.index(null_building)] = self.building
        else:
            player.game.normal_buildings.append(self.building)
        self.building.owner = player
        self.building.worker = None
        player.points += self.building.points
        
    def __repr__(self):
        return '%s->[%s]' % (format_resources(self.input), self.building)

class CastleAction(TradeAction):
    def __init__(self, res1, res2):
        TradeAction.__init__(self, input={'food':1, res1:1, res2:1}, output={})
        
    def __repr__(self):
        return '%s->Castle' % format_resources(self.input)

class Decision(object):
    pass

class ActionDecision(Decision):
    ''' A decision is a choice between a number of actions '''
    def __init__(self, actions):
        self.actions = actions
        
class WorkerDecision(Decision):
    def __init__(self, buildings):
        self.buildings = buildings
        self.buildings = [None] + self.buildings 



class Building(object):
    ''' A simple building has a static list of actions the player may choose from '''
    def __init__(self, name, *actions):
        self.name = name
        self.actions = actions
        
    def activate(self, player):
        actions = [action for action in self.actions if action.can_execute(player)]
        return ActionDecision(actions)
        #if len(actions) == 0:
        #    return
        #elif len(actions) == 1:
        #    print actions
        #    actions[0].execute(player)
        #else:
        #    print actions
        
    def constructable(self, points, **cost):
        self.cost = cost
        self.points = points
        return self
            
    def __repr__(self):
        return '/'.join([str(action) for action in self.actions if not isinstance(action, NullAction)])
    
class NullBuilding(Building):
    def activate(self, player):
        return ActionDecision(NullAction())
    def __eq__(self, other):
        return isinstance(other, NullBuilding)
        
class MarketBuilding(Building):
    ''' A market building allows the sale of any resource for money'''
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.actions = [TradeAction({resource:1}, {'money':amount}) for resource in RESOURCES]
        self.actions.append(NullAction())
    def __repr__(self):
        return 'R->%d' % self.amount

class PeddlerBuilding(Building):
    ''' A peddler building allows the purchase of any resource for money'''
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.actions = [TradeAction({'money':amount}, {resource:1}) for resource in RESOURCES if resource != 'gold']
        self.actions.append(NullAction())
    def __repr__(self):
        return '%d->R' % self.amount
    
class GuildBuilding(Building):
    def __init__(self, name):
        self.name = name
        self.actions = [MoveProvostAction(i) for i in [-3, -2, -1, 0, 1, 2, 3]]
    def __repr__(self):
        return 'Prov'
    
class CarpenterBuilding(Building):
    def __init__(self, name):
        self.name = name
        self.actions = []
        for building in wood_buildings:
            if 'any' in building.cost: # Ugh, have to deal with being able to construct some buildings with anything
                for resource in RESOURCES:
                    new_cost = {}
                    for key, value in building.cost.items():
                        if key == 'any':
                            new_cost[resource] = new_cost.get(resource,0) + value
                        else:
                            new_cost[key] = new_cost.get(key,0) + value
                    self.actions.append(ConstructAction(building, new_cost))
            else:
                self.actions.append(ConstructAction(building, building.cost))
    def __repr__(self):
        return 'Carpenter'
    
class CastleBuilding(Building):
    def __init__(self):
        self.name = 'Castle'
        self.actions = [CastleAction('wood', 'stone'), CastleAction('wood', 'cloth'), CastleAction('cloth', 'stone'),
                        CastleAction('wood', 'gold'), CastleAction('stone', 'gold'), CastleAction('cloth', 'gold'), NullAction()]

    def __repr__(self):
        return 'Castle'
    
     

castle = CastleBuilding()   
trading_post = Building("Trading Post", ProduceAction(money=3))
merchant_guild = GuildBuilding("Merchant's Guild")
joust_field = Building("Joust Field",JoustAction(), NullAction())

wood_farm_food = Building("Farm",ProduceAction(food=2), ProduceAction(cloth=1)).constructable(2, wood=1, food=1)
wood_farm_cloth = Building("Farm",ProduceAction(cloth=2), ProduceAction(food=1)).constructable(2, wood=1, food=1)
wood_quarry = Building("Quarry", ProduceAction(stone=2)).constructable(2, wood=1, food=1)
wood_sawmill = Building("Sawmill", ProduceAction(wood=2)).constructable(2, wood=1, food=1)
wood_market = MarketBuilding("Market", 6).constructable(2, wood=1, any=1)
wood_peddler = PeddlerBuilding("Peddler", 1).constructable(2, wood=1, any=1)

wood_buildings = [wood_farm_food, wood_farm_cloth, wood_quarry, wood_sawmill, wood_market, wood_peddler]



neutral_farm = Building("Farm",ProduceAction(food=1), ProduceAction(cloth=1))
neutral_forest = Building("Forest",ProduceAction(food=1), ProduceAction(wood=1))
neutral_sawmill = Building("Sawmill", ProduceAction(wood=1))
neutral_quarry = Building("Quarry", ProduceAction(stone=1))
neutral_market = MarketBuilding("Market", 4)
neutral_carpenter = CarpenterBuilding("Carpenter")

fixed_peddler = PeddlerBuilding("Peddler", 2)
fixed_carpenter = CarpenterBuilding("Carpenter")
fixed_gold = Building("Gold Mine", ProduceAction(gold=1))



special_buildings = [castle, trading_post, merchant_guild]
neutral_buildings = [neutral_carpenter, neutral_farm, neutral_forest, neutral_sawmill, neutral_quarry, neutral_market]
fixed_buildings = [fixed_peddler, fixed_carpenter]

null_building = NullBuilding("Null")

if __name__ == '__main__':
    from player import *
    player = Player(None, None)
    print wood_quarry.activate(player).actions
    #print player
    #print merchant_guild