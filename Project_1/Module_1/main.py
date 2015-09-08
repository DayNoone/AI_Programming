# coding=utf-8
import math
from heapq import heappush, heappop
from Node import Node
from generateBoard import generateBoard

MOVEMENT_COST = 1


def calculateHValue(xPos, yPos, goalNode):
    xOff = math.fabs(goalNode.xPos - xPos)
    yOff = math.fabs(goalNode.yPos - yPos)
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
        print "newX", newX, "newY", newY
        if boardWidth > newX >= 0 and boardHeight > newY >= 0:
            print "INSIDE board"
            if board[newX][newY] != '#':
                newNode = Node(parent, calculateGValue(parent), calculateHValue(newX, newY, goalNode), newX, newY)
                succ.append(newNode)
        print ""
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


def best_first_search(initNode, goalNode, board):
    closedNodes = []
    openNodes = []
    initNode.set_gValue(calculateGValue(initNode))
    initNode.set_hValue(calculateHValue(initNode, goalNode))

    heappush(openNodes, initNode)

    while True:
        if openNodes.count() == 0:
            print "No solution found"
            break
        x = heappop(openNodes)
        heappush(closedNodes, x)
        if x.xPos == goalNode.xPos and x.xPos == goalNode.yPos:
            print "Solution found!"
            break

        succ = generate_all_successors(x, board, goalNode)

        for s in succ:
            """TODO: If node S* has previously been created, and if state(S*) = state(S), then S ← S*."""
            x.kids.append(s)
            if s not in (closedNodes or openNodes):
                attach_and_eval(s, x)
                heappush(openNodes, s)
            elif x.gValue + MOVEMENT_COST < s.gValue:
                attach_and_eval(s, x)
                if s in closedNodes:
                    propagate_path_improvements()


board = generateBoard(6, 6, 1, 0, 5, 5, [[3, 2, 2, 2], [0, 3, 1, 3], [2, 0, 4, 2], [2, 5, 2, 1]])
goalNode = Node(None, None, None, 5, 5)
startNode = Node(None, calculateGValue(None), calculateHValue(1, 0, goalNode), 1, 0)
best_first_search(startNode, goalNode, board)


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
