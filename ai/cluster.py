from ai import AI
import collections
import random
import collections
import operator

class ClusterAI(AI):

    possibleAttacks = []

    '''def initial_placement(self, empty, remaining):
        if empty:
            return random.choice(empty)
        else:
            t = random.choice(list(self.player.territories))
            return t'''

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
            for prob,t,a,satk,sdef in targets: #dont loop through all
                tmp = self.heuristic(t,a,satk) 
                if tmp + (prob * 1000) > maxI:
                    maxI = tmp
                    src = t
                    dest = a
            return [[src,dest,self.haltAttack,self.moveTroops]]
            #return [[targets[0][1],targets[0][2],self.haltAttack, None]]
        else: return [(None, None, None, None)]

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result

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

    def heuristic(self, src, tgt, a_survive):
	temp_src_force = src.forces
	temp_src_owner = src.owner
	temp_tgt_force = tgt.forces
	temp_tgt_owner = tgt.owner
	tgt.owner = src.owner
	src.forces = a_survive
	tgt.forces = self.moveTroops(src.forces,src, tgt)
	src.forces = a_survive - self.moveTroops(src.forces,src, tgt)
	a_border = [t for t in temp_src_owner.territories if t.border]
	d_border = []
	for t in a_border:
	        for c in t.connect:
	                if t.owner != c.owner and c not in d_border:
	                        d_border.append(c)
	a_border_force = sum(a.forces for a in a_border)
	d_border_force = sum(d.forces for d in d_border)

	src.forces = temp_src_force
	src.owner  = temp_src_owner
	tgt.forces = temp_tgt_force
	tgt.owner  = temp_tgt_owner
	return a_border_force - d_border_force

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

    def initHeuristic(self, src):
	temp_src_force = src.forces
	src.owner      = self.player
	src.forces += 1
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
