# coding=utf-8
import math
from heapq import heappush, heappop
from Node import Node, NinjaNode
from generateBoard import getBoardExampleList, getBoardInfoFromInput
from gui import drawBoard, initiate


def updateStates(successors, states):
    for s in successors:
        if s.state not in states:
            states[s.state] = s


def calculateHeuristicValue(xPos, yPos, goalPos, heuristic):
    xOff = math.fabs(goalPos[0] - xPos)
    yOff = math.fabs(goalPos[1] - yPos)
    if heuristic == 1:
        return (xOff + yOff) * MOVEMENT_COST
    elif heuristic == 2:
        return math.sqrt(xOff * xOff + yOff * yOff) * MOVEMENT_COST
    else:
        return 0


def calculateGValue(parent):
    if parent is None:
        return 0
    return parent.gValue + MOVEMENT_COST


def generate_all_successors(parent, boardMatrix, ninjaMode):
    newChildPositions = [
        (parent.xPos + 1, parent.yPos),
        (parent.xPos - 1, parent.yPos),
        (parent.xPos, parent.yPos + 1),
        (parent.xPos, parent.yPos - 1)
    ]
    newChildren = []
    for newChildPosition in newChildPositions:
        if 0 <= newChildPosition[0] < len(boardMatrix) and 0 <= newChildPosition[1] < len(boardMatrix):
            if boardMatrix[newChildPosition[0]][newChildPosition[1]] != '#':
                if parent.parent is not None and parent.parent.xPos == newChildPosition[0] and parent.parent.yPos == \
                        newChildPosition[1]:
                    continue
                if ninjaMode:
                    newChildren.append(NinjaNode(parent, 0, 0, newChildPosition[0], newChildPosition[1]))
                else:
                    newChildren.append(Node(parent, 0, 0, newChildPosition[0], newChildPosition[1]))

    return newChildren


def propagate_path_improvements(parent):
    for child in parent.kids:
        if (parent.gValue + MOVEMENT_COST) < child.gValue:
            child.parent = parent
            child.set_gValue(calculateGValue(parent))
            propagate_path_improvements(child)


def attach_and_eval(child, parent, goalPos, heuristic):
    child.parent = parent
    child.set_gValue(parent.gValue + MOVEMENT_COST)
    child.set_hValue(calculateHeuristicValue(child.xPos, child.yPos, goalPos, heuristic))


def searchAlgorithm(goalPos, board, algorithm, heuristic, ninjaMode, debug=False):
    closedNodes = []
    openNodes = []
    states = {}
    initNode = Node(None, 0, 0, board.startXY[0], board.startXY[1])
    if ninjaMode:
        initNode = NinjaNode(None, 0, 0, board.startXY[0], board.startXY[1])
    initNode.set_gValue(0)
    initNode.set_hValue(calculateHeuristicValue(initNode.xPos, initNode.yPos, goalPos, heuristic))

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

        drawBoard(x, board.boardMatrix, board.startXY, board.goalXY, openNodes, closedNodes, False)

        heappush(closedNodes, x)

        if x.xPos == goalPos[0] and x.yPos == goalPos[1]:
            print "Solution found!"
            return x, openNodes, closedNodes

        successors = generate_all_successors(x, board.boardMatrix, ninjaMode)

        if debug:
            print "len(successors):", len(successors)
            for a in successors:
                print a

        updateStates(successors, states)

        for s in successors:
            s = states[s.state]
            x.kids.append(s)
            if s not in closedNodes and s not in openNodes:
                attach_and_eval(s, x, goalPos, heuristic)
                if algorithm == 1:
                    heappush(openNodes, s)
                elif algorithm == 2:
                    openNodes.insert(0, s)
                elif algorithm == 3:
                    openNodes.append(s)

            elif x.gValue + MOVEMENT_COST < s.gValue:
                attach_and_eval(s, x, goalPos, heuristic)
                if s in closedNodes:
                    propagate_path_improvements(s)


def lengthSolution(x, length):
    if x.parent is not None:
        return lengthSolution(x.parent, length + 1)
    return length


def run(board, algorithm, heuristic, ninjaMode):
    initiate(board.boardMatrix)

    x, openNodes, closedNodes = searchAlgorithm(board.goalXY, board, algorithm, heuristic, ninjaMode, False)

    if x.xPos == board.goalXY[0] or x.yPos == board.goalXY[1]:
        print
        print "Results:"
        print "\tLength of solution:\t", lengthSolution(x, 0)
        print "\tSearched nodes:\t\t", len(openNodes) + len(closedNodes)
        print "\t\tOpen nodes:\t\t", len(openNodes)
        print "\t\tClosed nodes:\t", len(closedNodes)

    drawBoard(x, board.boardMatrix, board.startXY, board.goalXY, openNodes, closedNodes, True)




MOVEMENT_COST = 1

# (.   \
#    \  |
#     \ |___(\--/)
#   __/    (  . . )
#  "'._.    '-.O.'
#       '-.  \ "|\
#          '.,,/'.,,


def inputValidation(inputText):
    while True:
        try:
            return int(raw_input(inputText))
        except ValueError:
            print('Please enter an integer...')


def main():
    boardList = getBoardExampleList()

    board = inputValidation('Choose board (0-5) (9 - custom): ')

    algorithm = inputValidation('Choose from algorithms: A* (1), Depth-first (2), Breadth-first (3): ')

    heuristic = inputValidation('Choose from heuristics: Manhattan (1), Euclidean (2), No heuristic/Dijkstra (3): ')

    node = inputValidation('Choose from nodes: Normal Node (1), Ninja Node (2): ')

    ninjaMode = False;
    if node == 2:
        ninjaMode = True

    if board == 9:
        selectedBoard = getBoardInfoFromInput()
    else:
        selectedBoard = boardList[board]

    run(selectedBoard, algorithm, heuristic, ninjaMode)

    print ""

while True:
    main()
