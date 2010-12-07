import json
from game import *

def player_to_json(player):
    info = {}
    attrs = ['name', 'resources', 'favors', 'section_batches', 'workers', 'passed']
    for attr in attrs:
        info[attr] = getattr(player, attr)
    return info

def building_to_json(building):
    if not building:
        return None
    info = {}
    info['class'] = building.__class__.__name__
    info['name'] = building.name
    info['owner'] = None if not building.owner else building.owner.name
    info['worker'] = None if not building.worker else building.owner.name
    info['repr'] = repr(building)

    return info

def game_to_json(game):
    info = {}
    attrs = ['turn', 'phase', 'step', 'section', 'bailiff', 'provost',
                    'pass_order', 'stables_order', 'castle_order']
    for attr in attrs:
        info[attr] = getattr(game, attr)
    info['players'] = []
    info['buildings'] = []
    for player in game.players:
        info['players'].append(player_to_json(player))
    for building in game.buildings:
        info['buildings'].append(building_to_json(building))
    return json.dumps(info)
    
def action_to_json(action):
    return {'class':action.__class__.__name__, 'repr':repr(action)}
    
def decision_to_json(decision):
    info = {}
    info['class'] = decision.__class__.__name__
    info['player'] = decision.player.name
    if hasattr(decision, 'buildings'):
        info['buildings'] = []
        for building in decision.buildings:
            info['buildings'].append(building_to_json(building))
    if hasattr(decision, 'tracks'):
        info['tracks'] = []
        for track in decision.tracks:
            info['buildings'].append(get_track_name(track))
    if hasattr(decision, 'actions'):
        info['actions'] = []
        for action in decision.actions:
            info['actions'].append(action_to_json(action))
    return json.dumps(info)
    
class JSONDecisionPlayer(Player):
    def make_decision(self, decision):
        print decision_to_json(decision)
        self.game.make_decision(decision, 0)
    
if __name__ == '__main__':
    
    game = Game(1, JSONDecisionPlayer)
    game.begin_turn()
    
    data = game_to_json(game)
    print data
    print len(data)
    
    game.step_game()