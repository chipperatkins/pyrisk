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

    """def continueAttack(self):
        if self.attack():
            return True
        else: return False"""

    def getAttacks(self):   
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    prob, satk, sdef = self.simulate(t.forces, a.forces)
                    #if t.forces > a.forces:
                    if prob > 0.50:
                        yield (t, a)
    
    def attack(self):
        for t,a in self.getAttacks():
            yield (t,a,None,None)

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result
