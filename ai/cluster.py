from ai import AI
import random
import collections
from copy import deepcopy


class ClusterAI(AI):
    """
    StupidAI: Plays a completely random game, randomly choosing and reinforcing
    territories, and attacking wherever it can without any considerations of wisdom.
    """
    def initial_placement(self, empty, remaining):
        if empty:
            return random.choice(empty)
        else:
            t = random.choice(list(self.player.territories))
            return t

    def attack(self):
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    if t.forces > a.forces:
                        yield (t, a, None, None)

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result

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
# create toy world for simulation
	        toy = deepcopy(self.world)
	        toy_players = set(t.owner for t in toy.territories.values())
	        toy_us = toy.territories[src.name].owner
#		print "Here is toy_us:"
#		print toy_us
	
	        numTroops = self.moveTroops(src, tgt)
	        toy.territories[src.name].forces = a_survive - numTroops
	
	# change ownership of target territory
	        toy.territories[tgt.name].forces = numTroops
	        toy.territories[tgt.name].owner = toy_us
	# find attacking and defending borders
		a_border = [t for t in toy_us.territories if t.border]
#		for t in toy_us.territories: print t.owner
	        d_border = []
	        for t in a_border:
	                for c in t.connect:
	                        if t.owner != c.owner and c not in d_border:
	                                d_border.append(c)
	# sum forces on borders
	        a_border_force = sum(a.forces for a in a_border)
	        d_border_force = sum(d.forces for d in d_border)
		
#		print "A border: " 
#		print a_border
#		print "D border: " 
#		print d_border
#		print "A force: " 
#		print a_border_force
#		print "D force: "
#		print d_border_force 
	# return difference of attacking and defending borders
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
	                
