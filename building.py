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
        
    def execute(self, player):
        player.game.move_provost(spaces)
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

class CastleAction(TradeAction):
    def __init__(self, res1, res2):
        TradeAction.__init__(self, input={'food':1, res1:1, res2:1}, output={})
        
    def execute(self, player):
        player.remove_resources(self.input)
        player.points += 5
        
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
            
    def __repr__(self):
        return '/'.join([str(action) for action in self.actions if not isinstance(action, NullAction)])
        
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

neutral_farm = Building("Farm",ProduceAction(food=1), ProduceAction(cloth=1))
neutral_forest = Building("Forest",ProduceAction(food=1), ProduceAction(wood=1))
neutral_sawmill = Building("Sawmill", ProduceAction(wood=1))
neutral_quarry = Building("Quarry", ProduceAction(stone=1))
neutral_market = MarketBuilding("Market", 4)

fixed_peddler = PeddlerBuilding("Peddler", 2)

wood_farm_food = Building("Farm",ProduceAction(food=2), ProduceAction(cloth=1))
wood_farm_cloth = Building("Farm",ProduceAction(cloth=2), ProduceAction(food=1))
wood_quarry = Building("Quarry", ProduceAction(stone=2))
wood_sawmill = Building("Sawmill", ProduceAction(wood=2))
wood_market = MarketBuilding("Market", 6)
wood_peddler = PeddlerBuilding("Peddler", 1)



special_buildings = [castle, trading_post]
neutral_buildings = [neutral_farm, neutral_forest, neutral_sawmill, neutral_quarry, neutral_market]
fixed_buildings = [fixed_peddler]
wood_buildings = [wood_farm_food, wood_farm_cloth, wood_quarry, wood_sawmill, wood_market, wood_peddler]

if __name__ == '__main__':
    from player import *
    player = Player(None)
    player.add_resources({'cloth':1})
    print player
    joust_field.activate(player)
    print player
    print merchant_guild