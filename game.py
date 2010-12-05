import random
from player import *
from textinterface import *
#from building import *

class Game(object):
    def __init__(self, players=2, player_class=Player):
        self.num_players = players
        self.players = []
        for i in range(self.num_players):
            player = player_class(self, COLORS[i])
            self.players.append(player)
        
        self.turn = -1

        
        self.special_buildings = special_buildings
        self.normal_buildings = []
        
        random.shuffle(neutral_buildings)
        self.normal_buildings += neutral_buildings
        self.normal_buildings += fixed_buildings
        self.normal_buildings += [NullBuilding("Null")] * 7
        self.normal_buildings += [fixed_gold]
        
        self.buildings = self.special_buildings + self.normal_buildings
        for building in self.buildings:
            building.owner = None
            
        self.wood_buildings = wood_buildings
        
        self.bailiff = INITIAL_BAILIFF
        self.provost = INITIAL_BAILIFF
        
    def begin_turn(self):
        self.turn += 1
        self.phase = 0
        self.step = 0
        self.pass_order = []
        self.castle_order = []
        self.castle_batches = []
        for player in self.players:
            player.passed = False
            player.workers = 6
        self.buildings = self.special_buildings + self.normal_buildings
        for building in self.buildings:
            building.worker = None
        
    def step_game(self):
        if self.turn == -1:
            self.begin_turn()
        if self.phase == PHASE_INCOME:
            for player in self.players:
                player.money += 2
            self.phase += 1 # No decisions in the income phase; proceed immediately
        if self.phase == PHASE_PLACE:
            if len([player for player in self.players if not player.passed]) == 0:
                self.phase += 1
                self.step = 0
            else:
                current_player = self.players[self.step % self.num_players]
                while current_player.passed:
                    self.step += 1
                    current_player = self.players[self.step % self.num_players]
                available_buildings = [building for building in self.buildings \
                                       if building.worker is None and \
                                       not isinstance(building, NullBuilding) and \
                                       player.money >= self.placement_cost(building, player) and\
                                       player.workers > 0 and\
                                       (not isinstance(building, CastleBuilding) or player not in self.castle_order)]
                if not available_buildings:
                    self.make_decision(WorkerDecision([None]), 0) # Automatically pass
                else:
                    current_player.make_decision(WorkerDecision(available_buildings))
        def common_step_buildings(buildings):
            if self.step == len(buildings):
                self.phase += 1
                self.step = 0
            else:
                building = buildings[self.step]
                if not building.worker:
                    self.step += 1
                    self.step_game()
                else:
                    decision = building.activate(building.worker)
                    if len(decision.actions) == 0:
                        self.step_game()
                    elif len(decision.actions) == 1:
                        self.make_decision(decision, 0)
                    else:
                        building.worker.make_decision(decision)
        if self.phase == PHASE_SPECIAL:
            common_step_buildings(self.special_buildings)
        if self.phase == PHASE_PROVOST:
            self.phase += 1
            self.step = 0
        if self.phase == PHASE_BUILDINGS:
            common_step_buildings([b for i, b in enumerate(self.normal_buildings) if i <= self.provost])
        if self.phase == PHASE_CASTLE:
            if self.step == len(self.castle_order):
                self.phase += 1
                self.step = 0
            else:
                player = self.castle_order[self.step]
                decision = castle.activate(player)
                if len(decision.actions) == 1:
                    self.make_decision(decision, 0)
                else:
                    player.make_decision(decision)
        if self.phase == PHASE_CASTLE_FAVOR:
            if self.step == 1:
                self.phase += 1
                self.step = 0
            else:
                if not self.castle_batches:
                    self.phase += 1
                    #self.step_game()
                else:
                    largest = max(self.castle_batches)
                    if largest != 0:
                        i = self.castle_batches.index(largest)
                        self.award_favor(self.castle_order[i])
        if self.phase == PHASE_END:
            self.bailiff += 2 if self.provost > self.bailiff else 1
            self.provost = self.bailiff
            self.begin_turn()
        
            
        
    def make_decision(self, decision, i):
        if isinstance(decision, FavorTrackDecision):
            track = favor_tracks[i]
            player = decision.player
            player.favors[i] += 1
            if i > 1: # VP and money tracks have no point to selecting lower cells
                actions = [] # Collect together all the actions
                for building in track[:player.favors[i]+1]:
                    actions.extend(building.activate(player).actions)
            else:
                actions = track[player.favors[i]].activate(player).actions
            decision = FavorDecision(player, actions)
            if len(decision.actions) == 1:
                self.make_decision(decision, 0)
            else:
                player.make_decision(decision)
            return
        if isinstance(decision, FavorDecision):
            player = decision.player
            action = decision.actions[i]
            action.execute(player)
            self.step += 1
            self.step_game()
            return
        if self.phase == PHASE_PLACE:
            player = self.players[self.step % self.num_players]
            building = decision.buildings[i]
            if building is None:
                if not self.pass_order:
                    player.money += 1
                self.pass_order.append(player)
                player.passed = True
            else:
                if isinstance(building, CastleBuilding):
                    self.castle_order.append(player)
                    self.castle_batches.append(0)
                else:
                    building.worker = player
                player.money -= self.placement_cost(building, player)
                player.workers -= 1
            self.step += 1
            self.step_game()
        elif self.phase == PHASE_SPECIAL:
            player = self.special_buildings[self.step].worker
            action = decision.actions[i]
            action.execute(player)
            self.step += 1
            self.step_game()
        elif self.phase == PHASE_BUILDINGS:
            player = self.normal_buildings[self.step].worker
            action = decision.actions[i]
            action.execute(player)
            self.step += 1
            self.step_game()
        elif self.phase == PHASE_CASTLE:
            player = self.castle_order[self.step]
            action = decision.actions[i]
            action.execute(player)
            if isinstance(action, NullAction):
                self.step += 1
            else:
                self.castle_batches[i] += 1
                player.points += 5
            self.step_game()
            
    def award_favor(self, player):
        decision = FavorTrackDecision(player)
        player.make_decision(decision)
            
    def placement_cost(self, building, player):
        '''Amount it will cost for a player to take a building'''
        if not self.pass_order:
            return 1
        if building.owner == player:
            return 1
        if self.num_players == 2 and self.pass_order:
            return 3
        return len(self.pass_order) + 1
        
if __name__ == '__main__':
    game = Game(players=1, player_class=TextPlayer)
    while True:
        game.step_game()
        print game.players[0]