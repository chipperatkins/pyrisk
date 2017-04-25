from ai import AI
import random
import collections

class BetterClusterAI(AI):
    """
    BetterAI: Thinks about what it is doing a little more - picks a priority
    continent and priorities holding and reinforcing it.
    """
    def start(self):
        self.area_priority = list(self.world.areas)
        random.shuffle(self.area_priority)

    def priority(self):
        priority = sorted([t for t in self.player.territories if t.border], 
                          key=lambda x: self.area_priority.index(x.area.name))
        priority = [t for t in priority if t.area == priority[0].area]
        return priority if priority else list(self.player.territories)
            

    def initial_placement(self, empty, available):
        if empty:
            empty = sorted(empty, key=lambda x: self.area_priority.index(x.area.name))
            return empty[0]
        else:
            return random.choice(self.priority())

    def reinforce(self, available):
        priority = self.priority()
        result = collections.defaultdict(int)
        while available:
            result[random.choice(priority)] += 1
            available -= 1
        return result

    def freemove(self):
        srcs = sorted([t for t in self.player.territories if not t.border], 
                      key=lambda x: x.forces)
        if srcs:
            src = srcs[-1]
            n = src.forces - 1
            return (src, self.priority()[0], n)
        return None

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
            '''for prob,t,a,satk,sdef in targets: #dont loop through all
                tmp = self.heuristic(t,a,satk) 
                if tmp + (prob * 1000) > maxI:
                    maxI = tmp
                    src = t
                    dest = a'''
            return [[src,dest,self.haltAttack,None]]
            #return [[targets[0][1],targets[0][2],self.haltAttack, None]]
        else: return [(None, None, None, None)]
