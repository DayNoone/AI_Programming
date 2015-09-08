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


def best_first_search(initNode, goalNode, board):
    closedNodes = []
    openNodes = []
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
        if x.xPos == goalNode[0] and x.xPos == goalNode[1]:
            print "Solution found!"
            return x

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


#board = generateBoard(6, 6, 1, 0, 5, 5, [[3, 2, 2, 2], [0, 3, 1, 3], [2, 0, 4, 2], [2, 5, 2, 1]])
board = generateBoard(20, 20, 19, 3, 2, 18, [[5, 5, 10, 10], [1, 2, 4, 1]])
initiate(board)
goalNode = (2, 18)
startNode = Node(None, calculateGValue(None), calculateHValue(1, 0, goalNode), 1, 0)
x = best_first_search(startNode, goalNode, board)
drawBoard(x, board, True)

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
