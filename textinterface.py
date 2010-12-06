from player import *

class TextPlayer(Player):
    
    def pretty_resources(self):
        out = ''
        for resource in RESOURCES:
            out += resource[0].upper() * self.resources[resource]
            if out and out[-1] != ' ':
                out += ' '
        return out
    
    def get_decision(self, max):
        while True:
            text = raw_input('Your decision:')
            try:
                i = int(text)
                if 0 <= i <= max:
                    return i
            except:
                pass
                    
    
    def make_decision(self, decision):
        if isinstance(decision, WorkerDecision):
            print '%s Placing worker.' % self.name
            print 'Workers:%d Money:%d Resources:%s' % (self.workers, self.money, self.pretty_resources())
            print '  #  O  W  P     Effect'
            print '  0              Pass'
            print
            i = 1
            j = -1
            first_normal_building = self.game.normal_buildings[0]
            for building in self.game.buildings :
                if j != -1:
                    j += 1
                if building == first_normal_building:
                    j = 0
                d = '   '
                if building in decision.buildings:
                    d = i
                    i += 1
                    
                owner = '-' if not building.owner else building.owner.initial
                if isinstance(building, InnBuilding):
                    owner = '-' if not self.game.inn_player else self.game.inn_player.initial
                worker = '-' if not building.worker else building.worker.initial
                if building == castle:
                    worker = ''.join([p.initial for p in self.game.castle_order])
                if building == stables:
                    worker = ''.join([p.initial for p in self.game.stables_order])
                provost = 'O' if j == self.game.provost else ' '
                    
                print '%3s%3s%3s%3s     %s' % (d,owner,worker,provost,building)
            #for i, building in enumerate(decision.buildings):
            #    print '%d: %s' % (i, building)
            i = self.get_decision(len(decision.buildings)-1)
            self.game.make_decision(decision, i)
        elif isinstance(decision, ActionDecision):
            print 
            print '%s taking action' % (self.name)
            for i, action in enumerate(decision.actions):
                print '%d: %s' % (i, action)
            i = self.get_decision(len(decision.actions)-1)
            print
            self.game.make_decision(decision, i)
        elif isinstance(decision, FavorTrackDecision):
            print
            print '%s selecting favor' % self.name
            for i, track in enumerate(decision.tracks):
                print '%d: %s' % (i, get_track_name(track))
            i = self.get_decision(len(decision.tracks)-1)
            print
            self.game.make_decision(decision, i)