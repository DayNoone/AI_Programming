from heapq import heappush, heappop


def addSuccessorsToState(successors, states):
    for s in successors:
        if s.state not in states:
            states[s.state] = s


def propagate_path_improvements(parent):
    for child in parent.kids:
        if (parent.gValue + child.MOVEMENT_COST) < child.gValue:
            child.parent = parent
            child.set_gValue(child.calculateGValue(parent))
            propagate_path_improvements(child)


def attach_and_eval(child, parent):
    child.parent = parent
    child.set_gValue(parent.gValue + child.MOVEMENT_COST)
    child.set_hValue(child.calculateHeuristicValue())


def searchAlgorithm(board, algorithm, heuristic, ninjaMode, initNode, debug=False):
    closedNodes = []
    openNodes = []
    states = {}

    initNode.set_gValue(0)
    initNode.set_hValue(initNode.calculateHeuristicValue())

    heappush(openNodes, initNode)

    while True:

        if debug:
            print
            print "#####"
            print "NEW WHILE"
            print "#####"
            print "Open nodes:", len(openNodes)
            print "Closed nodes:", len(closedNodes)
            print "States:", len(states)

        if len(openNodes) == 0:
            print "No solution found"
            return closedNodes[-1], openNodes, closedNodes

        if debug:
            print
            print "Open nodes: "
            for a in openNodes:
                print a
            print

        if debug:
            print
            print "Closed nodes: "
            for a in closedNodes:
                print a
            print

        if algorithm == 1:
            openNodes.sort()
            x = heappop(openNodes)
        else:
            x = openNodes.pop(0)

        if debug:
            print "Popped node:", x

        # x.drawBoard(x, board.boardMatrix, board.startXY, board.goalXY, openNodes, closedNodes, False)

        heappush(closedNodes, x)

        if x.checkIfGoalState():
            print "Solution found!"
            return x, openNodes, closedNodes

        successors = x.generate_all_successors()

        if debug:
            print "len(successors):", len(successors)
            for a in successors:
                print a

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
