RESOURCES = ['food', 'wood', 'stone', 'cloth', 'gold']
COLORS = ['Blue','Red','Green','Orange','Black']

def format_resources(resources):
    out = []
    for resource, amount in resources.items():
        if resource == 'money':
            out += [str(amount)]
        else:
            out += [resource[0].upper()] * amount
    out.sort()
    return ''.join(out)
    
PHASES = range(8)
    
PHASE_INCOME = 0
PHASE_PLACE = 1
PHASE_SPECIAL = 2
PHASE_PROVOST = 3
PHASE_BUILDINGS = 4
PHASE_CASTLE = 5
PHASE_CASTLE_FAVOR = 6
PHASE_SCORING = 7
PHASE_END = 8

INITIAL_BAILIFF = 10
SCORE_DUNGEON = 11
SCORE_WALLS = 17
SCORE_TOWERS = 23
LAST_SPACE = 27

SECTION_DUNGEON = 0
SECTION_WALLS = 1
SECTION_TOWERS = 2
SECTION_OVER = -1

SECTION_SPACES = [6, 10, 14]
SECTION_POINTS = [5, 4, 3]
