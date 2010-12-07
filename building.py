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
    
class BribeProvostAction(Action):
    def __init__(self, spaces):
        self.spaces = spaces
        
    def can_execute(self, player):
        return 0 < player.game.provost + self.spaces < LAST_SPACE and player.money >= abs(self.spaces)
        
    def execute(self, player):
        player.game.provost += self.spaces
        player.money -= abs(self.spaces)
        
        
    def __repr__(self):
        return '%d->P%+d' % (abs(self.spaces), self.spaces)
       
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
        player.game.decision_stack.append(FavorTrackDecision(player))
        
        
    def __repr__(self):
        return '%s->RF' % format_resources(self.input)
        
class ConstructAction(TradeAction):
    def __init__(self, building, cost):
        self.building = building
        TradeAction.__init__(self, input=cost, output={})
        
    def can_execute(self, player):
        # Prevent double construction of buildings
        return TradeAction.can_execute(self, player) and self.building in (player.game.wood_buildings + player.game.stone_buildings)
        
    def execute(self, player):
        player.remove_resources(self.input)
        if self.building in player.game.wood_buildings:
            player.game.wood_buildings.remove(self.building)
        if self.building in player.game.stone_buildings:
            player.game.stone_buildings.remove(self.building)
        if null_building in player.game.normal_buildings:
            player.game.normal_buildings[player.game.normal_buildings.index(null_building)] = self.building
        else:
            player.game.normal_buildings.append(self.building)
        self.building.owner = player
        self.building.worker = None
        player.game.log('%s gains %d points from building construction', player, self.building.points)
        player.points += self.building.points
        if hasattr(self.building, 'favors'):
            player.game.log('%s gains %d royal favors from building construction', player, self.building.favors)
            for i in range(self.building.favors):
                player.game.decision_stack.append(FavorTrackDecision(player))
        
    def __repr__(self):
        return '%s->[%s]' % (format_resources(self.input), self.building)

class CastleAction(TradeAction):
    def __init__(self, res1, res2):
        TradeAction.__init__(self, input={'food':1, res1:1, res2:1}, output={})
        
    def __repr__(self):
        return '%s->Castle' % format_resources(self.input)
        
class LawyerAction(TradeAction):
    def __init__(self, target, discount=False):
        self.target = target
        if discount:
            TradeAction.__init__(self, input={'cloth':1}, output={})
        else:
            TradeAction.__init__(self, input={'cloth':1, 'money':1}, output={})
        
    def can_execute(self, player):
        for i, residence in player.game.delayed_lawyer:
            if i == player.game.normal_buildings.index(self.target):
                return False # Someone has already transformed our target building
        return TradeAction.can_execute(self, player) 
        
    def execute(self, player):
        player.remove_resources(self.input)
        i = player.game.normal_buildings.index(self.target)
        residence = ResidenceBuilding()
        # Always delay the action just in case
        player.game.delayed_lawyer.append([i, residence])
        #player.game.normal_buildings[i] = residence
        residence.owner = player
        player.points += 2
        player.game.log('%s gains 2 points from residence construction', player)
        if hasattr(self.target, 'cost'): # Place constructable buildings back in the pool
            if 'wood' in self.target.cost.keys():
                player.game.wood_buildings.append(self.target)
            if 'stone' in self.target.cost.keys():
                player.game.stone_buildings.append(self.target)

        
    def __repr__(self):
        return '[%s]->[Residence]' % self.target

class ArchitectAction(TradeAction):
    def __init__(self, target, result):
        self.target = target
        self.result = result
        TradeAction.__init__(self, input=self.result.cost, output={})
        
    def execute(self, player):
        player.remove_resources(self.input)
        i = player.game.normal_buildings.index(self.target)
        player.game.normal_buildings[i] = self.result
        self.result.owner = player
        player.game.prestige_buildings.remove(self.result)
        player.game.log('%s gains %d points from prestige building construction', player, self.result.points)
        player.points += self.result.points
        if hasattr(self.result, 'favors'):
            player.game.log('%s gains %d royal favors from prestige building construction', player, self.result.favors)
            for i in range(self.result.favors):
                player.game.decision_stack.append(FavorTrackDecision(player))
                
    def __repr__(self):
        return '[Residence]+%s->[Prestige](%dP %dF %dI)' % (format_resources(self.input),
                                             self.result.points, self.result.favors, self.result.income)

class FavorAction(Action):
    ''' A favor action allows the player to select from a number of favors on one track'''
        
    def __init__(self, building):
        self.building = building
        
    def execute(self, player):
        decision = self.building.activate(player)
        player.game.decision_stack.append(FavorDecision(player, decision.actions)) # Cast to FavorDecision
        
    def __repr__(self):
        return repr(self.building)

class GateAction(Action):
    def __init__(self, target):
        self.target = target
        
    def execute(self, player):
        if isinstance(self.target, CastleBuilding):
            player.game.castle_order.append(player)
            player.game.castle_batches.append(0)
        elif isinstance(self.target, StablesBuilding):
            player.game.stables_order.append(player)
        else:
            self.target.worker = player
        
    def __repr__(self):
        return 'Worker->[%s]' % self.target
    
class RemoveWorkerFromInnAction(Action):
    def execute(self, player):
        player.game.inn_player = None
        player.game.log("%s removes their worker from the inn", player)
        
    def __repr__(self):
        return 'Remove worker from inn'

class Decision(object):
    def filter_actions(self):
        pass

class ActionDecision(Decision):
    ''' A decision is a choice between a number of actions '''
    def __init__(self, player, actions):
        self.player = player
        self.actions = actions
    def filter_actions(self):
        self.actions = [action for action in self.actions if action.can_execute(self.player)]
        
class WorkerDecision(Decision):
    def __init__(self, player, buildings):
        self.player = player
        self.buildings = buildings
        self.buildings = [None] + self.buildings
        
class FavorTrackDecision(Decision):
    def __init__(self, player):
        self.player = player
        
    @property
    def tracks(self):
        current_time = (self.player.game.turn, self.player.game.phase)
        if current_time != self.player.when_used:
            self.player.when_used = current_time
            self.player.tracks_used = []
        return [track for track in favor_tracks if track not in self.player.tracks_used]
            
        

class FavorDecision(ActionDecision):
    def __init__(self, player, actions):
        self.player = player
        self.actions = actions

class Building(object):
    ''' A simple building has a static list of actions the player may choose from '''
    def __init__(self, name, *actions):
        self.name = name
        self.actions = actions
        self.worker = None
        self.owner = None
        
    def activate(self, player):
        actions = [action for action in self.actions if action.can_execute(player)]
        return ActionDecision(player, actions)
        #if len(actions) == 0:
        #    return
        #elif len(actions) == 1:
        #    print actions
        #    actions[0].execute(player)
        #else:
        #    print actions
        
    def can_activate(self, player):
        return True
        
    def constructable(self, points, **cost):
        self.cost = cost
        self.points = points
        return self
    
    def awards_favors(self, num):
        self.favors = num
        return self
            
    def __repr__(self):
        return '/'.join([str(action) for action in self.actions if not isinstance(action, NullAction)])
    
class UnusableBuilding(Building):
    pass
    
class NullBuilding(UnusableBuilding):
    def activate(self, player):
        return ActionDecision(player, [NullAction()])
    def __eq__(self, other):
        return isinstance(other, NullBuilding)
        
class IncomeBuilding(Building):
    pass
        
class ResidenceBuilding(IncomeBuilding, UnusableBuilding):
    def __init__(self):
        self.name = 'Residence'
        self.income = 1
        
    def __repr__(self):
        return 'Residence [+1]'
    
class PrestigeBuilding(UnusableBuilding):
    def __init__(self, name):
        self.name = name
        self.favors = 0
        self.income = 0
        
    def __repr__(self):
        return 'Prestige' 
    
class PrestigeIncomeBuilding(IncomeBuilding, PrestigeBuilding):
    def __init__(self, name, income):
        self.name = name
        self.favors = 0
        self.income = income
        
    def __repr__(self):
        return 'Prestige [+%d]' % ( self.income)
        
class MarketBuilding(Building):
    ''' A market building allows the sale of any resource for money'''
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.actions = [TradeAction({resource:1}, {'money':amount}) for resource in RESOURCES]
        self.actions.insert(0, NullAction())
    def __repr__(self):
        return 'R->%d' % self.amount

class PeddlerBuilding(Building):
    ''' A peddler building allows the purchase of any resource for money'''
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.actions = [TradeAction({'money':amount}, {resource:1}) for resource in RESOURCES if resource != 'gold']
        self.actions.insert(0, NullAction())
    def __repr__(self):
        return '%d->R' % self.amount
    
class GuildBuilding(Building):
    def __init__(self, name):
        self.name = name
        self.actions = [MoveProvostAction(i) for i in [-3, -2, -1, 0, 1, 2, 3]]
    def __repr__(self):
        return 'Prov'
    
class CarpenterBuilding(Building):
    def __init__(self, name, discount=False):
        self.name = name
        self.actions = [NullAction()]
        for building in wood_buildings:
            cost = building.cost.copy()
            if discount:
                del cost['wood']
            if 'any' in cost: # Ugh, have to deal with being able to construct some buildings with anything
                for resource in RESOURCES:
                    new_cost = {}
                    for key, value in cost.items():
                        if key == 'any':
                            new_cost[resource] = new_cost.get(resource,0) + value
                        else:
                            new_cost[key] = new_cost.get(key,0) + value
                    self.actions.append(ConstructAction(building, new_cost))
            else:
                self.actions.append(ConstructAction(building, cost))
    def __repr__(self):
        return 'Carpenter'
    
class MasonBuilding(Building):
    def __init__(self, name, discount=False):
        self.name = name
        self.actions = [NullAction()]
        for building in stone_buildings:
            cost = building.cost.copy()
            if discount:
                del cost['stone']
            self.actions.append(ConstructAction(building, cost))
    def __repr__(self):
        return 'Mason'
    
class LawyerBuilding(Building):
    def __init__(self, name, discount=False):
        self.name = name
        self.discount = discount
    def activate(self, player): # Transformable building must be dynamically found
        buildings = [building for building in player.game.normal_buildings if \
                        (building.owner == None or building.owner == player) and not hasattr(building, 'fixed') \
                        and not isinstance(building, LawyerBuilding) and not isinstance(building, NullBuilding)]
        self.actions = [NullAction()]
        for building in buildings:
            self.actions.append(LawyerAction(building, discount=self.discount))
        return Building.activate(self, player) # Let's still take advantage of the superclass filtering
    def __repr__(self):
        return 'Lawyer'
 
class ArchitectBuilding(Building):
    def __init__(self, name):
        self.name = name
        
    def activate(self, player):
        buildings = [building for building in player.game.normal_buildings if \
                     isinstance(building, ResidenceBuilding) and building.owner == player]
        if not buildings: # No buildings to transform
            return ActionDecision(player, [NullAction()])
        self.actions = [NullAction()]
        for result in player.game.prestige_buildings:
            self.actions.append(ArchitectAction(buildings[0], result))
        return Building.activate(self, player)
        
    def __repr__(self):
        return 'Architect'
    
class GateBuilding(Building):
    
    def activate(self, player):
        available_buildings = player.game.available_buildings(player, cost=False)
        self.actions = [GateAction(building) for building in available_buildings]
        return Building.activate(self, player)
            
    
    def __repr__(self):
        return 'Gate'
    
class InnBuilding(Building):
    
    def __init__(self):
        self.name = 'Inn'
    def __repr__(self):
        return 'Inn'
        
class StablesBuilding(Building):
    def __init__(self):
        self.name = 'Stables'
    def __repr__(self):
        return 'Stables'
   
class BribeProvostBuilding(Building):
    def __init__(self):
        self.actions = [NullAction()]
        self.actions += [BribeProvostAction(spaces) for spaces in [-3,-2,-1,1,2,3]]
   
class CastleBuilding(Building):
    def __init__(self):
        self.name = 'Castle'
        self.actions = [NullAction(), CastleAction('wood', 'stone'), CastleAction('wood', 'cloth'), CastleAction('cloth', 'stone'),
                        CastleAction('wood', 'gold'), CastleAction('stone', 'gold'), CastleAction('cloth', 'gold')]

    def __repr__(self):
        return 'Castle'
    
class CompoundBuilding(Building):
    ''' A compound building allows the player, or possibly different players, to make multiple decisions.
        Forms the basis of stone farms and other complex buildings '''
    def __init__(self, name, *decisions):
        self.name = name
        self.decisions = decisions
        
    def activate(self, player):
        first = self.decisions[0]
        last = self.decisions[-1]
        for i, decision in enumerate(self.decisions):
            decision.player = self.deciding_player(i)
            decision.filter_actions()
        for decision in reversed(self.decisions):
            if decision != first and decision.player != None:
                player.game.decision_stack.append(decision)
        return first
        
    def deciding_player(self, i):
        ''' Who will make the ith decision for this building?'''
        return self.worker
    
    def __repr__(self):
        return '(Undefined)'
    
class WoodPeddlerBuilding(CompoundBuilding):
    def __init__(self):
        actions = [TradeAction({'money':1}, {resource:1}) for resource in RESOURCES if resource != 'gold']
        CompoundBuilding.__init__(self, 'Peddler', ActionDecision(None, actions), ActionDecision(None, actions))
    def __repr__(self):
        return '1->R/2->RR'
    
class StoneAlchemistBuilding(CompoundBuilding):
    def __init__(self):
        actions = []
        for one in RESOURCES:
            for two in RESOURCES:
                if one == 'gold' or two == 'gold':
                    continue
                cost = {}
                cost[one] = 1
                cost[two] = cost.get(two, 0) + 1
                actions.append(TradeAction(cost, {'gold':1}))
        actions.append(NullAction())
        CompoundBuilding.__init__(self, 'Alchemist', ActionDecision(None, actions), ActionDecision(None, actions))
    def __repr__(self):
        return 'RR->G/RRRR->GG'
    
class StoneProductionBuilding(CompoundBuilding):
    ''' A stone farm, in addition to providing resource to its worker, may provide a choice
    of resources to the owner if different from the worker'''
    def __init__(self, name, production):
        self.production = production
        one, two = production.keys()
        CompoundBuilding.__init__( self, name, \
            ActionDecision(None, [ProduceAction(**production)]), \
            ActionDecision(None, [ProduceAction(**{one:1}), ProduceAction(**{two:1})]))
        
    def deciding_player(self, i):
        if i == 0: # Worker gets the basic production
            return self.worker
        if i == 1 and self.worker != self.owner: # Allow owner to pick their bonus resource
            return self.owner
        return None # Worker was = to owner, no bonus
    
    def __repr__(self):
        one, two = self.production.keys()
        return format_resources(self.production) + ' (%s/%s)' % (one[0].upper(), two[0].upper())
        
class ResourceTrackTwoForOneBuilding(CompoundBuilding):
    def __init__(self):
        lose_one = ActionDecision(None, [TradeAction({resource:1},{}) for resource in RESOURCES])
        gain_one = ActionDecision(None, [ProduceAction(**{resource:1}) for resource in RESOURCES if resource != 'gold'])
        CompoundBuilding.__init__(self, None, lose_one, gain_one, gain_one)
        
    def can_activate(self, player):
        for resource in RESOURCES:
            if player.resources[resource] > 0:
                return True
        return False
    
    def activate(self, player):
        self.player = player
        return CompoundBuilding.activate(self, player)
    
    def deciding_player(self, player):
        return self.player
        
    def __repr__(self):
        return 'RR->R'

castle = CastleBuilding()
gate = GateBuilding("Gate")
trading_post = Building("Trading Post", ProduceAction(money=3))
merchant_guild = GuildBuilding("Merchant's Guild")
joust_field = Building("Joust Field",NullAction(), JoustAction())
inn = InnBuilding()
stables = StablesBuilding()

bribe_provost = BribeProvostBuilding()

prestige_statue = PrestigeBuilding("Statue").constructable(7, stone=2, gold=1).awards_favors(1)
prestige_granary = PrestigeBuilding("Granary").constructable(10, food=3, gold=1)
prestige_weaver = PrestigeBuilding("Weaver").constructable(12, cloth=3, gold=1)
prestige_theater = PrestigeBuilding("Theater").constructable(14, wood=3, gold=2).awards_favors(1)
prestige_college = PrestigeBuilding("College").constructable(14, stone=3, gold=2).awards_favors(1)
prestige_monument = PrestigeBuilding("Monument").constructable(14, stone=4, gold=2).awards_favors(2)
prestige_cathedral = PrestigeBuilding("Cathedral").constructable(25, stone=5, gold=3)
prestige_library = PrestigeIncomeBuilding("Library", income=1).constructable(10, wood=3, gold=1)
prestige_hotel = PrestigeIncomeBuilding("Hotel", income=2).constructable(16, stone=3, gold=2)

prestige_buildings = [prestige_statue, prestige_granary, prestige_weaver, prestige_theater, prestige_college,
                      prestige_monument, prestige_cathedral, prestige_library, prestige_hotel]

stone_tailor = Building("Tailor", NullAction(), TradeAction({'cloth':2}, {'points':4}), TradeAction({'cloth':3},{'points':6})).constructable(6, stone=1, wood=1)
stone_church = Building("Church", NullAction(), TradeAction({'money':2}, {'points':3}), TradeAction({'money':4},{'points':5})).constructable(3, stone=1, cloth=1).awards_favors(1)
stone_bank = Building("Bank", NullAction(), TradeAction({'money':2}, {'gold':1}), TradeAction({'money':5},{'gold':2})).constructable(6, stone=1, wood=1)
stone_jeweler = Building("Jeweler", NullAction(), TradeAction({'gold':1}, {'points':5}), TradeAction({'gold':2},{'points':9})).constructable(6, stone=1, cloth=1)
stone_alchemist = StoneAlchemistBuilding().constructable(6, wood=1, stone=1)
stone_farm = StoneProductionBuilding("Farm", {'food':2, 'cloth':1}).constructable(3, stone=1, food=1)
stone_park = StoneProductionBuilding("Park", {'wood':2, 'food':1}).constructable(3, stone=1, food=1)
stone_workshop = StoneProductionBuilding("Workshop", {'stone':2, 'cloth':1}).constructable(3, stone=1, food=1)
stone_architect1 = ArchitectBuilding("Architect").constructable(6, stone=1, food=1)
stone_architect2 = ArchitectBuilding("Architect").constructable(6, stone=1, food=1)


stone_buildings = [stone_church, stone_bank, stone_jeweler, stone_tailor, stone_alchemist,
                   stone_farm, stone_park, stone_workshop, stone_architect1, stone_architect2]

wood_farm_food = Building("Farm",ProduceAction(food=2), ProduceAction(cloth=1)).constructable(2, wood=1, food=1)
wood_farm_cloth = Building("Farm",ProduceAction(cloth=2), ProduceAction(food=1)).constructable(2, wood=1, food=1)
wood_quarry = Building("Quarry", ProduceAction(stone=2)).constructable(2, wood=1, food=1)
wood_sawmill = Building("Sawmill", ProduceAction(wood=2)).constructable(2, wood=1, food=1)
wood_market = MarketBuilding("Market", 6).constructable(2, wood=1, any=1)
wood_peddler = WoodPeddlerBuilding().constructable(2, wood=1, any=1)
wood_mason = MasonBuilding("Mason").constructable(4, wood=1, food=1)
wood_lawyer = LawyerBuilding("Lawyer").constructable(4, wood=1, cloth=1)

wood_buildings = [wood_farm_food, wood_farm_cloth, wood_quarry, wood_sawmill, wood_market, wood_peddler, wood_mason, wood_lawyer]



neutral_farm = Building("Farm",ProduceAction(food=1), ProduceAction(cloth=1))
neutral_forest = Building("Forest",ProduceAction(food=1), ProduceAction(wood=1))
neutral_sawmill = Building("Sawmill", ProduceAction(wood=1))
neutral_quarry = Building("Quarry", ProduceAction(stone=1))
neutral_market = MarketBuilding("Market", 4)
neutral_carpenter = CarpenterBuilding("Carpenter")

fixed_peddler = PeddlerBuilding("Peddler", 2)
fixed_peddler.fixed = True
fixed_carpenter = CarpenterBuilding("Carpenter")
fixed_carpenter.fixed = True
fixed_gold = Building("Gold Mine", ProduceAction(gold=1))
fixed_gold.fixed = True



special_buildings = [castle, gate, trading_post, merchant_guild, joust_field, stables, inn]
neutral_buildings = [neutral_carpenter, neutral_farm, neutral_forest, neutral_sawmill, neutral_quarry, neutral_market]
fixed_buildings = [fixed_peddler, fixed_carpenter]

null_building = NullBuilding("Null")




point_track = [Building(None, ProduceAction(points=p)) for p in range(1, 6)]
money_track = [Building(None, ProduceAction(money=m)) for m in range(3, 8)]
resource_track = [Building(None, ProduceAction(food=1)), Building(None, ProduceAction(wood=1), ProduceAction(stone=1)),
                  Building(None, ProduceAction(cloth=1)),ResourceTrackTwoForOneBuilding(),Building(None, ProduceAction(gold=1))]
building_track = [Building(None, NullAction()), CarpenterBuilding(None, discount=True), MasonBuilding(None, discount=True), LawyerBuilding(None, discount=True), ArchitectBuilding(None)]

favor_tracks = [point_track, money_track, resource_track, building_track]
track_names = ['Points', 'Money', 'Resource', 'Building']

def get_track_name(track):
    return track_names[favor_tracks.index(track)]

if __name__ == '__main__':
    from player import *
    player = Player(None, None)
    print wood_quarry.activate(player).actions
    #print player
    #print merchant_guild