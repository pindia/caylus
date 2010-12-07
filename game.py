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
            if self.num_players > 2 and i >= 1:
                player.money += 1
            if i >= 3:
                player.money += 1
            self.players.append(player)
        
        self.turn = -1
        self.section = SECTION_DUNGEON
        self.new_section = SECTION_DUNGEON
        self.spaces = SECTION_SPACES[:]
        self.inn_player = None

        
        self.special_buildings = special_buildings
        if players < 3:
            self.special_buildings.remove(stables)
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
        self.stone_buildings = stone_buildings
        self.prestige_buildings = prestige_buildings
        
        self.bailiff = INITIAL_BAILIFF
        self.provost = INITIAL_BAILIFF
        
    def begin_turn(self):
        self.turn += 1
        self.phase = 0
        self.step = 0
        self.pass_order = []
        self.stables_order = []
        self.castle_order = []
        self.castle_batches = []
        self.decision_stack = []
        self.delayed_lawyer = []
        for player in self.players:
            player.passed = False
            player.workers = 5 if self.inn_player == player else 6
        self.buildings = self.special_buildings + self.normal_buildings
        for building in self.buildings:
            building.worker = None
        
    def step_game(self):
        if self.turn == -1:
            self.begin_turn()
        if self.phase == PHASE_INCOME:
            for player in self.players:
                income = 2
                for building in self.normal_buildings:
                    if isinstance(building, IncomeBuilding) and building.owner == player:
                        income += building.income
                player.money += income
                self.log("%s receives income of %d", player, income)

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
                available_buildings = self.available_buildings(current_player)
                if not available_buildings:
                    self.make_decision(WorkerDecision(current_player, [None]), 0) # Automatically pass
                else:
                    current_player.make_decision(WorkerDecision(current_player, available_buildings))
        def common_step_buildings(buildings):
            if self.step == len(buildings):
                self.phase += 1
                self.step = 0
            else:
                building = buildings[self.step]
                if isinstance(building, InnBuilding):
                    if building.worker:
                        self.inn_player = building.worker
                        self.log("%s is the new inn owner", self.inn_player)
                        self.step += 1
                        self.step_game()
                    elif self.inn_player:
                        decision = ActionDecision(self.inn_player, [NullAction(), RemoveWorkerFromInnAction()])
                        self.inn_player.make_decision(decision)
                    else:
                        self.step += 1
                        self.step_game() 
                elif isinstance(building, int):
                    pass
                else:
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
            if self.step == len(self.players):
                self.phase += 1
                self.step = 0
            else:
                player = self.players[self.step]
                decision = bribe_provost.activate(player)
                if len(decision.actions) == 1:
                    self.make_decision(decision, 0)
                else:
                    player.make_decision(decision)
        if self.phase == PHASE_BUILDINGS:
            common_step_buildings([b for i, b in enumerate(self.normal_buildings) if i <= self.provost])
        if self.phase == PHASE_CASTLE:
            if self.step == len(self.castle_order):
                self.phase += 1
                self.step = 0
            else:
                player = self.castle_order[self.step]
                if self.spaces[-1]:
                    decision = castle.activate(player)
                else: # Castle is completely filled
                    decision = ActionDecision(player, [NullAction()])
                    player.penalty_immune = True # Player should not receive a penalty
                if len(decision.actions) == 1:
                    self.make_decision(decision, 0)
                else:
                    player.make_decision(decision)
        if self.phase == PHASE_CASTLE_FAVOR:
            if self.step == 1:
                self.phase += 1
                self.step = 0
            else:
                for i, player in enumerate(self.castle_order):
                    num = self.castle_batches[i]
                    if num == 0 and not hasattr(player, 'penalty_immune'):
                        self.log('%s is assessed 2 point penalty for not building', player)
                        player.points -= 2
                if not sum(self.castle_batches):
                    self.phase += 1
                    #self.step_game()
                else:
                    # Assess penalty for not building
                    # Award the favor
                    largest = max(self.castle_batches)
                    if largest != 0:
                        i = self.castle_batches.index(largest)
                        self.award_favor(self.castle_order[i])
        if self.phase == PHASE_SCORING:
            if self.step == 1:
                self.phase += 1
                self.step = 0
            else:
                self.bailiff += 2 if self.provost > self.bailiff else 1
                self.provost = self.bailiff
                def penalty(player, num):
                    self.log('%s is penalized %d points in scoring', player, num)
                    player.points -= num
                def award(player, num):
                    self.log('%s is awarded %d royal favors in scoring', player, num)
                    [self.decision_stack.append(FavorTrackDecision(player)) for i in range(num)]
                if self.section == SECTION_DUNGEON and (self.spaces[SECTION_DUNGEON] == 0 or self.bailiff >= SCORE_DUNGEON):
                    self.log('SCORING: Dungeon')
                    for player in self.players:
                        num = player.section_batches[SECTION_DUNGEON]
                        if num == 0:
                            penalty(player, 2)
                        if num >=2:
                            award(player, 1)
                    self.new_section = SECTION_WALLS
                if self.section == SECTION_WALLS and (self.spaces[SECTION_WALLS] == 0 or self.bailiff >= SCORE_WALLS):
                    self.log('SCORING: Walls')
                    for player in self.players:
                        num = player.section_batches[SECTION_WALLS]
                        if num == 0:
                            penalty(player, 3)
                        if num ==2:
                            award(player, 1)
                        if num == 3 or num == 4:
                            award(player, 2)
                        if num >= 5:
                            award(player, 3)
                    self.new_section = SECTION_TOWERS
                if self.section == SECTION_TOWERS and (self.spaces[SECTION_TOWERS] == 0 or self.bailiff >= SCORE_TOWERS):
                    self.log('SCORING: Towers')
                    for player in self.players:
                        num = player.section_batches[SECTION_TOWERS]
                        if num == 0:
                           penalty(player, 4)
                        if num == 2 or num == 3:
                            award(player, 1)
                        if num == 4 or num == 5:
                            award(player, 2)
                        if num >= 6:
                            award(player, 3)
                    self.new_section = SECTION_OVER
                if self.decision_stack: # If there were royal favors awarded, start presenting them
                    decision = self.decision_stack.pop()
                    decision.player.make_decision(decision)
                else:
                    self.phase += 1 # Scoring happened but no favors, continue
        if self.phase == PHASE_END:
            # Update section
            self.section = self.new_section
            # Perform delayed transformations
            for i, residence in self.delayed_lawyer:
                self.normal_buildings[i] = residence 
            self.delayed_lawyer = []
            # Activate stables
            for player in reversed(self.stables_order):
                self.players.remove(player)
                self.players.insert(0, player)
            if len(self.players) == 2:
                self.players.reverse()
            
            if self.section == SECTION_OVER:
                for player in self.players:
                    resources = 0
                    for resource in RESOURCES:
                        if resource != 'gold':
                            resources += player.resources[resource]
                    bonus = player.money // 4 + resources // 3 + player.resources['gold'] * 3
                    self.log('%s gains %d end-of-game points', player, bonus)
                    player.points += bonus
                self.phase = -1
                return
            self.begin_turn()
        
            
        
    def make_decision(self, decision, i):
        if isinstance(decision, FavorTrackDecision):
            player = decision.player
            if i == -1:
                self.log('%s cannot select any royal favor tracks', player)
                self.make_decision(FavorDecision(decision.player, [NullAction()]), 0)
                return
            track = decision.tracks[i]
            abs_index = favor_tracks.index(track)
            player.tracks_used.append(track)
            MAX_SPACE = [1, 3, 4]
            player.favors[abs_index] = min(player.favors[abs_index]+1, MAX_SPACE[self.section])
            self.log('%s selects favor track %s', player, get_track_name(track))
            if i > 1: # VP and money tracks have no point to selecting lower cells
                actions = [] # Collect together all the actions
                for building in track[:player.favors[abs_index]+1]:
                    #actions.extend(building.activate(player).actions)
                    if building.can_activate(player):
                        actions.append(FavorAction(building))
            else:
                actions = track[player.favors[abs_index]].activate(player).actions
            decision = FavorDecision(player, actions)
            if len(decision.actions) == 1:
                self.make_decision(decision, 0)
            else:
                player.make_decision(decision)
            return
        if isinstance(decision, FavorDecision):
            player = decision.player
            action = decision.actions[i]
            if not isinstance(action, FavorAction): # Don't log selection of space, only final action
                self.log('%s executes action %s via royal favor', player, action)
            action.execute(player)
            self.pop_decision_or_continue()
            return
        if self.phase == PHASE_PLACE:
            player = decision.player
            building = decision.buildings[i]
            if building is None: # Player passed
                self.log('%s passes', player)
                if not self.pass_order:
                    self.log('%s gains 1 denier from being first to pass', player)
                    player.money += 1
                self.pass_order.append(player)
                player.passed = True
            else:
                if isinstance(building, CastleBuilding):
                    self.castle_order.append(player)
                    self.castle_batches.append(0)
                elif isinstance(building, StablesBuilding):
                    self.stables_order.append(player)
                else:
                    building.worker = player
                    if building.owner and building.owner != player:
                        self.log('%s is awarded 1 point from owned building', building.owner)
                        building.owner.points += 1
                player.money -= self.placement_cost(building, player)
                player.workers -= 1
            self.step += 1
            self.step_game()
        elif self.phase == PHASE_PROVOST:
            player = decision.player
            action = decision.actions[i]
            if hasattr(action, 'spaces'):
                self.log('%s moves the provost %d spaces', player, action.spaces)
            action.execute(player)
            self.step += 1
            self.step_game()
        elif self.phase in [PHASE_SPECIAL, PHASE_BUILDINGS]:
            player = decision.player
            action = decision.actions[i]
            self.log('%s executes action %s', player, action)
            action.execute(player)
            self.pop_decision_or_continue()
        elif self.phase == PHASE_CASTLE:
            player = self.castle_order[self.step]
            action = decision.actions[i]
            action.execute(player)
            if isinstance(action, NullAction):
                self.step += 1
            else:
                self.castle_batches[self.castle_order.index(player)] += 1
                section = self.section
                if not self.spaces[self.section]:
                    section += 1 # Spill over to the next section
                player.points += SECTION_POINTS[section]
                self.log('%s scores %d points from submission of %s', player, SECTION_POINTS[section], format_resources(action.input))
                self.spaces[section] -= 1
                player.section_batches[section] += 1
                    
            self.step_game()
            
    def pop_decision_or_continue(self, step_after=True):
        ''' Call after a player's decision is processed. Pops a decision from the stack
        and presents it if available, or proceeds if not.'''
        if self.decision_stack:
            decision = self.decision_stack.pop()
            decision.filter_actions()
            if isinstance(decision, ActionDecision) and len(decision.actions) == 1:
                self.make_decision(decision, 0)
            elif isinstance(decision, FavorTrackDecision) and len(decision.tracks) == 1:
                self.make_decision(decision, 0)
            elif isinstance(decision, FavorTrackDecision) and len(decision.tracks) == 0:
                self.make_decision(decision, -1)
            else:
                decision.player.make_decision(decision)
        else:
            self.step += 1 # We're done with this building
            if step_after:
                self.step_game()
        
            
    def award_favor(self, player):
        decision = FavorTrackDecision(player)
        player.make_decision(decision)
            
    def available_buildings(self, player, cost=True):
        ''' Buildings that can have workers placed on them by a certain player.
            cost is whether or not to take into account placement cost. '''
        return [building for building in self.buildings \
                                       if building.worker is None and \
                                       not isinstance(building, UnusableBuilding) and \
                                       (not cost or player.money >= self.placement_cost(building, player)) and\
                                       (not cost or player.workers > 0) and\
                                       (not isinstance(building, CastleBuilding) or player not in self.castle_order)and\
                                       (not isinstance(building, StablesBuilding) or (player not in self.stables_order and len(self.stables_order) < 3)) \
                                    ]
            
    def placement_cost(self, building, player):
        '''Amount it will cost for a player to take a building'''
        if not self.pass_order:
            return 1
        if building.owner == player:
            return 1
        if self.inn_player == player:
            return 1
        if self.num_players == 2 and self.pass_order:
            return 3
        return len(self.pass_order) + 1
        
    def log(self, message, player=None, *args):
        if not player:
            print '[Log]' + message
        else:
            print '[Log]' + message % ((player.name,) + args)
        
if __name__ == '__main__':
    game = Game(players=2, player_class=TextPlayer)

    while game.section != SECTION_OVER:
        game.step_game()
    print 'GAME OVER'
    for player in game.players:
        print '%s: %d' % (player.name, player.points)