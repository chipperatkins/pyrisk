from ai import AI
import collections
import random

class ClusterAI(AI):

    possibleAttacks = []

    def initial_placement(self, empty, remaining):
        if empty:
            return random.choice(empty)
        else:
            t = random.choice(list(self.player.territories))
            return t

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
        if targets != []:
            return [[targets[0][1],targets[0][2],self.haltAttack, None]]
        else: return [(None, None, None, None)]

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result
