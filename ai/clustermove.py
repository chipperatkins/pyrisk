from ai import AI
import collections
import random
import collections
from copy import deepcopy

class ClusterMoveAI(AI):

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
        maxI = 0
        if targets != []:
            src = targets[0][1]
            dest = targets[0][2]
            for prob,t,a,satk,sdef in targets: #dont loop through all
                tmp = self.heuristic(t,a,satk) 
                if tmp + (prob * 1000) > maxI:
                    maxI = tmp
                    src = t
                    dest = a
            return [[src,dest,self.haltAttack,None]]
            #return [[targets[0][1],targets[0][2],self.haltAttack, None]]
        else: return [(None, None, None, None)]

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result


    """
    NEW Code STARTS HERE
    """
    def heuristic(self, src, tgt, a_survive):
        """ 
        This is a heuristic function defining the clusterer's behavior.
        The clusterer attempts to spread its influence from its strong borders. 
        It favors attacking territories that will reduce the enemy:owned troop ratio. 
        It will also favor taking nodes that it is likely to be able to capture.
        This behavior allows it to continue taking nodes even when taking a node might reduce
        the overall strength ratio of its border because it reduces the number of states on the border
        and also helps in projecting power.
        """
        toy = deepcopy(self.world)
        toy_players = set(t.owner for t in toy.territories.values())
        toy_us = toy.territories[src.name].owner
	
        numTroops = self.moveTroops(src.forces, src, tgt)
	toy.territories[src.name].forces = a_survive - numTroops
	
	toy.territories[tgt.name].forces = numTroops
	toy.territories[tgt.name].owner = toy_us
	a_border = [t for t in toy_us.territories if t.border]
	d_border = []
	for t in a_border:
	    for c in t.connect:
	        if t.owner != c.owner and c not in d_border:
	            d_border.append(c)
	a_border_force = sum(a.forces for a in a_border)
	d_border_force = sum(d.forces for d in d_border)
		
	return a_border_force - d_border_force
    def moveTroops(self, n_atk, source, target):
	""" 
	Moves troops under these conditions:
	if src and tgt have enemies, move half
	if src has no enemies, move all
	if tgt has no enemies, move 1
	Returns number of troops to move to destination
	"""
        if(self.checkEnemies(target, owner=source.owner)):
	    if(self.checkEnemies(source, threshold=1)):
	        return (n_atk-1) // 2
	    else:
	        return n_atk-1
	else:
	    return 1
	
    def checkEnemies(self, source, owner=None, threshold=0):
	enemies = 0
	if(owner == None): owner = source.owner
	for t in source.connect:
	    if t.owner != owner:
	        enemies += 1
	if enemies > threshold:
	    return True
        else:
	    return False