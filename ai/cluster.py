from ai import AI
import collections
import random

class ClusterAI(AI):

    def initial_placement(self, empty, remaining):
        if empty:
            return random.choice(empty)
        else:
            t = random.choice(list(self.player.territories))
            return t

    def continueAttack(self):
        l = []
        for t,a in self.getAttacks():
            l.append([t,a])
        #print(l)
        #print(len(l))
        if len(l) > 0:
            return True
        else: return False

    def getAttacks(self):   
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    prob, satk, sdef = self.simulate(t.forces, a.forces)
                    if prob > 0.5:
                        yield (t, a)
    
    def attack(self):
        for t,a in self.getAttacks(): #calling getAttacks twice, once here once in continue !!!
            yield (t,a,None,None)

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result
