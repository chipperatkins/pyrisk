

def clustererHeuristic(src, tgt, moveTroops):
	""" 
	This is a heuristic function defining the clusterer's behavior.
	The clusterer attempts to spread its influence from its strong borders. 
	It favors attacking territories that will reduce the enemy:owned troop ratio. 
	It will also favor taking nodes that it is likely to be able to capture.
	This behavior allows it to continue taking nodes even when taking a node might reduce
	the overall strength ratio of its border because it reduces the number of states on the border
	and also helps in projecting power.
	"""
	source = Territory(src)
	target = Territory(tgt)

# Not confident these borders are set correctly
	d_border = [t for t in self.player.territories if t.border]
	a_border = [t.connect for t in d_border if t.adjacent
	p_win, a_survive, d_survive = self.simulate(src.forces, tgt.forces)
	
	num_troops_move = moveTroops(source, target)
	a_border_force = sum(a.forces for a in a_border_forces) + a_survive
	d_border_force = sum(d.forces for d in d_border_forces) + d_survive

def moveTroops(src, tgt):
	""" 
	Moves troops under these conditions:
	if src and tgt have enemies, move half
	if src has no enemies, move all
	if tgt has no enemies, move 1
	"""
	if(src.hasEnemies()):
		if(tgt.hasEnemies()):
			tmp = (src.forces-1) // 2
			src.forces = src.forces // 2
			return (src.forces-1) // 2
		else:
			return 1
	else:
		return src.forces - 1
	
