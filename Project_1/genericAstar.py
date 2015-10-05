from heapq import heappush, heappop


def addSuccessorsToState(successors, states):
	for s in successors:
		if s.state not in states:
			states[s.state] = s


def propagate_path_improvements(parent):
	for child in parent.kids:
		if (parent.gValue + child.MOVEMENT_COST) < child.gValue:
			child.parent = parent
			child.set_gValue(child.calculateGValue())
			propagate_path_improvements(child)


def attach_and_eval(child, parent):
	child.parent = parent
	child.set_gValue(parent.gValue + child.MOVEMENT_COST)
	child.set_hValue(child.calculateHeuristicValue())


def searchAlgorithm(algorithm, initNode):
	closedNodes = []
	openNodes = []
	states = {}

	initNode.set_gValue(0)
	initNode.set_hValue(initNode.calculateHeuristicValue())

	heappush(openNodes, initNode)

	while True:
		if len(openNodes) == 0:
			print "No solution found"
			return closedNodes[-1], openNodes, closedNodes

		if algorithm == 1:
			openNodes.sort()
			x = heappop(openNodes)
		else:
			x = openNodes.pop(0)

		print "heuristic:", x.hValue
		if x.hValue >= 10000000:
			print "No solution found"
			return closedNodes[-1], openNodes, closedNodes
		x.drawBoard(openNodes, closedNodes, False)

		heappush(closedNodes, x)

		if x.checkIfGoalState():
			print "Solution found!"
			return x, openNodes, closedNodes

		successors = x.generate_all_successors()

		addSuccessorsToState(successors, states)

		for s in successors:
			s = states[s.state]
			x.kids.append(s)
			if s not in closedNodes and s not in openNodes:
				attach_and_eval(s, x)
				if algorithm == 1:
					heappush(openNodes, s)
				elif algorithm == 2:
					openNodes.insert(0, s)
				elif algorithm == 3:
					openNodes.append(s)

			elif x.gValue + x.MOVEMENT_COST < s.gValue:
				attach_and_eval(s, x)
				if s in closedNodes:
					propagate_path_improvements(s)