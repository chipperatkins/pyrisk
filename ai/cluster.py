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
        l = []
        for t,a in self.getAttacks():
            l.append([t,a])
        if len(l) > 0:
            return True
        else: return False

    def getAttacks(self, caller=1):   #delete caller if needed
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    prob, satk, sdef = self.simulate(t.forces, a.forces)
                    if prob > 0.66 and caller == 0:
                        yield (t, a)
                    elif prob > 0.5 and caller != 0:
			yield (t,a)

    def attack(self,idx):
        for t,a in self.getAttacks(): #calling getAttacks twice, once here once in continue !!!
            yield (t,a,None,None)

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result
