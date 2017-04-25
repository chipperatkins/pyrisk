from ai import AI
import random
import collections
from copy import deepcopy
from time import sleep
import operator

class ClusterAI(AI):
    """
    StupidAI: Plays a completely random game, randomly choosing and reinforcing
    territories, and attacking wherever it can without any considerations of wisdom.
    """
    def initial_placement(self, empty, remaining):

	if not empty:	
		hold = []
		for t in self.player.territories:
			hold = [j for j in t.connect if j.owner == None]
		terrHeur = {}
		for t in hold:
		    terrHeur[t] = self.initHeuristic(t)
		if not terrHeur:
			choice = []
			for j in self.player.territories:
				choice += [j]
			return random.choice(choice).name
		return max(terrHeur.iteritems(), key=operator.itemgetter(1))[0]

	if not (self.player.territories):
		return random.choice(empty)
		
	territories = set(self.player.territories)
	nearby = set()

	for t in territories:
		hold = [j for j in t.connect if j.owner == None]
		for h in hold:
		    if h not in nearby:
		    	nearby.add(h)
	terrHeur = {}
	for t in nearby:
	    terrHeur[t] = self.initHeuristic(t)
	if not terrHeur:
		return random.choice(empty)
	return max(terrHeur.iteritems(), key=operator.itemgetter(1))[0]

    def attack(self):
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
		    p, a_survive, d = self.simulate(t.forces,a.forces)
		    h = self.heuristic(t,a,int(a_survive))
                    if h > 0 or p > .6:
                        yield (t, a, None, None)

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result

    def heuristic(self, src, tgt, a_survive):
# cluster heuristic

# store local state
		temp_src_force = src.forces
		temp_src_owner = src.owner
		temp_tgt_force = tgt.forces
		temp_tgt_owner = tgt.owner

# update local state to t+1
		tgt.owner = src.owner
		src.forces = a_survive
		tgt.forces = self.moveTroops(src, tgt)
		src.forces = a_survive - self.moveTroops(src, tgt)

# find attacking and defending borders
		a_border = [t for t in temp_src_owner.territories if t.border]
	        d_border = []
	        for t in a_border:
	                for c in t.connect:
	                        if t.owner != c.owner and c not in d_border:
	                                d_border.append(c)

	# sum forces on borders
	        a_border_force = sum(a.forces for a in a_border)
	        d_border_force = sum(d.forces for d in d_border)

	# return difference of attacking and defending borders
		src.forces = temp_src_force
		src.owner  = temp_src_owner
		tgt.forces = temp_tgt_force
		tgt.owner  = temp_tgt_owner
	        return a_border_force - d_border_force
	
    def moveTroops(self, source, target):
	        """ 
	        Moves troops under these conditions:
	        if src and tgt have enemies, move half
	        if src has no enemies, move all
	        if tgt has no enemies, move 1
	        Returns number of troops to move to destination
	        """
	        if(self.checkEnemies(target, owner=source.owner)):
	                if(self.checkEnemies(source, threshold=1)):
#	                        print "First case"
	                        return (source.forces-1) // 2
	                else:
#	                        print "Second case"
	                        return source.forces-1
	        else:
#	                print "Third case"
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
	                

    def initHeuristic(self, src):
# cluster heuristic

# store local state
		temp_src_force = src.forces
		src.owner      = self.player

# update local state to t+1
		src.forces += 1

# find attacking and defending borders
		a_border = [t for t in src.owner.territories if t.border]
	        d_border = []
	        for t in a_border:
	                for c in t.connect:
	                        if t.owner != c.owner and c not in d_border:
	                                d_border.append(c)

	# sum forces on borders
	        a_border_force = sum(a.forces for a in a_border)
	        d_border_force = sum(d.forces for d in d_border)

	# return difference of attacking and defending borders
		src.forces = temp_src_force
		src.owner = None
	        return a_border_force - d_border_force
	
