# coding=utf-8
import math
from heapq import heappush, heappop
from Node import Node
from generateBoard import generateBoard
from gui import drawBoard, initiate

MOVEMENT_COST = 1


def calculateHValue(xPos, yPos, goalNode):
    xOff = math.fabs(goalNode[0] - xPos)
    yOff = math.fabs(goalNode[1] - yPos)
    return xOff + yOff


def calculateGValue(parent):
    if parent is None:
        return 0
    return parent.gValue + MOVEMENT_COST


def generate_all_successors(parent, board, goalNode):
    succ = []

    boardWidth = len(board[0])
    boardHeight = len(board)

    directionX = [0, 0, 1, -1]
    directionY = [1, -1, 0, 0]

    for direction in range(len(directionX)):
        newX = parent.xPos + directionX[direction]
        newY = parent.yPos + directionY[direction]
        if parent.xPos == newX and parent.yPos == newY:
            continue
        if boardWidth > newX >= 0 and boardHeight > newY >= 0:
            if board[newX][newY] != '#':
                newNode = Node(parent, calculateGValue(parent), calculateHValue(newX, newY, goalNode), newX, newY)
                succ.append(newNode)
    return succ


def propagate_path_improvements(parent):
    for child in parent.kids:
        if (parent.gValue + MOVEMENT_COST) < child.gValue:
            child.parent = parent
            child.set_gValue(calculateGValue(parent))
            propagate_path_improvements(child)


def attach_and_eval(child, parent):
    child.parent = parent
    child.set_gValue(parent.gValue + MOVEMENT_COST)
    calculateHValue(child.xPos, child.yPos, goalNode)


def updateStates(succ, states):
    for s in succ:
        string = str(s.xPos) + str(999) + str(s.yPos) + str(999) + str(s.gValue)
        s.state = int(string)
        states[s.state] = s


def best_first_search(initNode, goalNode, board):
    closedNodes = []
    openNodes = []
    states = {}
    initNode.set_gValue(calculateGValue(initNode))
    initNode.set_hValue(calculateHValue(initNode.xPos, initNode.yPos, goalNode))

    heappush(openNodes, initNode)

    while True:
        if len(openNodes) == 0:
            print "No solution found"
            break
        x = heappop(openNodes)
        drawBoard(x, board, False)
        heappush(closedNodes, x)
        if x.xPos == goalNode[0] and x.yPos == goalNode[1]:
            print "Solution found!"
            return x

        succ = generate_all_successors(x, board, goalNode)
        updateStates(succ, states)

        for s in succ:
            # TODO: If node S* has previously been created, and if state(S*) = state(S), then S ← S*.
            if s.state in states.keys():
                print "s.state:", s.state
                if s.state == states[s.state].state:
                    "THE SAME!"
                s = states[s.state]
            else:
                "NOT"
            x.kids.append(s)
            if s not in (closedNodes or openNodes):
                attach_and_eval(s, x)
                heappush(openNodes, s)
            elif x.gValue + MOVEMENT_COST < s.gValue:
                print "ELFI!!!"
                attach_and_eval(s, x)
                if s in closedNodes:
                    propagate_path_improvements()


board5 = generateBoard(20, 20, 0, 0, 19, 13, [[4, 0, 4, 16], [12, 4, 2, 16], [16, 8, 4, 4]])
# board2 = generateBoard(20, 20, 0, 0, 19, 19,[[17, 10, 2, 1], [14, 4, 5, 2], [3, 16, 10, 2], [13, 7, 5, 3], [15, 15, 3, 3]])
# board = generateBoard(6, 6, 1, 0, 5, 5, [[3, 2, 2, 2], [0, 3, 1, 3], [2, 0, 4, 2], [2, 5, 2, 1]])
# board = generateBoard(20, 20, 19, 3, 2, 18, [[5, 5, 10, 10], [1, 2, 4, 1]])
initiate(board5)
goalNode = (19, 13)
startNode = Node(None, calculateGValue(None), calculateHValue(0, 0, goalNode), 0, 0)
x = best_first_search(startNode, goalNode, board5)
drawBoard(x, board5, True)


# Tests
def generateSuccTest():
    global succ
    testBoard = [['O' for x in range(5)] for x in range(5)]
    testBoard[0][1] = '#'
    succ = generate_all_successors(Node(None, 0, 0, 1, 1),
                                   testBoard,
                                   Node(None, 0, 0, 0, 0))
    print "Length of succ:"
    print len(succ)

# generateSuccTest()
