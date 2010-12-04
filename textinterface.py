from player import *

class TextPlayer(Player):
    
    def pretty_resources(self):
        out = ''
        for resource in RESOURCES:
            out += resource[0].upper() * self.resources[resource]
            if out and out[-1] != ' ':
                out += ' '
        return out
    
    def make_decision(self, decision):
        if isinstance(decision, WorkerDecision):
            print '%s Placing worker.' % self.name
            print 'Workers:%d Money:%d Resources:%s' % (self.workers, self.money, self.pretty_resources())
            print '  #  O  W  P     Effect'
            print '  0              Pass'
            print
            i = 1
            provost_building = self.game.normal_buildings[self.game.provost]
            for building in self.game.buildings :
                d = '   '
                if building in decision.buildings:
                    d = i
                    i += 1
                print '%3s%3s%3s%3s     %s' % (d,
                                               '-' if not building.owner else building.owner.initial,
                                               '-' if not building.worker else building.worker.initial,
                                               'O' if building == provost_building else ' ', building)
            #for i, building in enumerate(decision.buildings):
            #    print '%d: %s' % (i, building)
            i = int(raw_input('Your decision:'))
            self.game.make_decision(decision, i)
        elif isinstance(decision, ActionDecision):
            print '%s taking action' % (self.name)
            for i, action in enumerate(decision.actions):
                print '%d: %s' % (i, action)
            i = int(raw_input('Your decision:'))
            self.game.make_decision(decision, i)