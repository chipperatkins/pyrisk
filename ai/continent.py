from ai import AI
from collections import defaultdict
import random

class ContinentAI(AI):
    area_priority = ['Australia', 'South America', 'North America', 
                     'Africa', 'Europe', 'Asia']

    def initial_placement(self, empty, remaining):
        if empty:
            owned_by_area = defaultdict(int)
            for t in self.world.territories.values():
                if t.owner == self.player:
                    owned_by_area[t.area.name] += 1
            for area in owned_by_area:
                if owned_by_area[area] == len(self.world.areas[area].territories) - 1:
                    remain = [e for e in empty if e.area.name == area]
                    if remain:
                        return random.choice(remain)
            return sorted(empty, key=lambda x: self.area_priority.index(x.area.name))[0]
        else:
            priority = []
            i = 0
            while not priority:
                priority = [t for t in self.player.territories if t.area.name == self.area_priority[i] and t.border]
                i += 1
            return random.choice(priority)
            
    def reinforce(self, available):
        priority = []
        i = 0
        while not priority:
            priority = [t for t in self.player.territories if t.area.name == self.area_priority[i] and t.border]
            i += 1
        reinforce_each = available / len(priority)
        remain = available - reinforce_each * len(priority)
        result = {p: reinforce_each for p in priority}
        result[priority[0]] += remain
        return result

    def freemove(self):
        for t in self.player.territories:
            for adjE in t.adjacent(friendly=False):
                if adjE.forces > t.forces:
                    for adjF in t.adjacent(friendly=True):
                        if adjF.forces > 1:
                            return (adjF, t, adjF.forces-1)
    def continueAttack(self):
        l = self.getAttacks()
        if l != []:
            return True
        else:
            return False

    def getAttacks(self, caller=1):   #delete caller if needed
        targets = []
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    prob, satk, sdef = self.simulate(t.forces, a.forces)
                    if prob > 0.66 and caller == 0:
                        targets.append([prob,t,a])
                    elif prob > 0.5 and caller != 0:
                        targets.append([prob,t,a,satk,sdef])
        targets.sort(reverse=True)
        return targets

    numAttacks = 0
    def haltAttack(self,atk, dfn):
        if self.numAttacks == 0:
            self.numAttacks += 1
            return True
        else:
            self.numAttacks = 0
            return False

    def attack(self,idx): #remove index
        targets = self.getAttacks() # calling get attacks twice here and continueAttack, fix!!
        maxI = 0
        atk = 0
        if targets != []:
            src = targets[0][1]
            dest = targets[0][2]
            return [[src,dest,self.haltAttack,None]]
        else: return [(None, None, None, None)]

