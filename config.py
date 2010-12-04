RESOURCES = ['food', 'wood', 'stone', 'cloth', 'gold']

def format_resources(resources):
    out = []
    for resource, amount in resources.items():
        if resource == 'money':
            out += [str(amount)]
        else:
            out += [resource[0].upper()] * amount
    out.sort()
    return ''.join(out)
    
PHASES = range(7)
    
PHASE_INCOME = 0
PHASE_PLACE = 1
PHASE_SPECIAL = 2
PHASE_PROVOST = 3
PHASE_BUILDINGS = 4
PHASE_CASTLE = 5
PHASE_END = 6
