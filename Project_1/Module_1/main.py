# coding=utf-8
import math
from heapq import heappush, heappop
from Node import Node
from Board import Board
from generateBoard import generateBoard
from gui import drawBoard, initiate


def calculateHValue(xPos, yPos, goalPos):
    xOff = math.fabs(goalPos[0] - xPos)
    yOff = math.fabs(goalPos[1] - yPos)
    return xOff + yOff


def calculateGValue(parent):
    if parent is None:
        return 0
    return parent.gValue + MOVEMENT_COST


def generate_all_successors(parent, board, goalPos):
    succ = []

    boardWidth = len(board[0])
    boardHeight = len(board)

    directionX = [0, 0, 1, -1]
    directionY = [1, -1, 0, 0]

    for direction in range(len(directionX)):
        newX = parent.xPos + directionX[direction]
        newY = parent.yPos + directionY[direction]

        if parent.parent is not None and parent.parent.xPos == newX and parent.parent.yPos == newY:
            continue
        if boardWidth > newX >= 0 and boardHeight > newY >= 0:
            if board[newX][newY] != '#':
                newNode = Node(parent, calculateGValue(parent), calculateHValue(newX, newY, goalPos), newX, newY)
                succ.append(newNode)

    print "Succs for parent ", parent
    for a in succ:
        print a
    return succ


def propagate_path_improvements(parent):
    print "propagate_path_improvements"
    for child in parent.kids:
        if (parent.gValue + MOVEMENT_COST) < child.gValue:
            child.parent = parent
            child.set_gValue(calculateGValue(parent))
            propagate_path_improvements(child)


def attach_and_eval(child, parent, goalPos):
    child.parent = parent
    child.set_gValue(parent.gValue + MOVEMENT_COST)
    child.set_hValue(calculateHValue(child.xPos, child.yPos, goalPos))


def updateStates(succ, states):
    for s in succ:
        string = str(s.xPos) + str(s.yPos)
        s.state = int(string)
        if s.state not in states:
            states[s.state] = s


def best_first_search(initNode, goalPos, board):
    closedNodes = []
    openNodes = []
    states = {}
    initNode.set_gValue(calculateGValue(initNode))
    initNode.set_hValue(calculateHValue(initNode.xPos, initNode.yPos, goalPos))

    heappush(openNodes, initNode)

    while True:
        print
        print "#####"
        print "NEW WHILE"
        print "#####"
        print "Open nodes:", len(openNodes)
        print "Closed nodes:", len(closedNodes)
        print "States:", len(states)
        if len(openNodes) == 0:
            print "No solution found"
            return initNode
        openNodes.sort()
        print
        print "Open nodes: "
        for a in openNodes:
            print a
        print
        x = heappop(openNodes)
        print "Popped node:", x
        drawBoard(x, board, False)
        heappush(closedNodes, x)
        if x.xPos == goalPos[0] and x.yPos == goalPos[1]:
            print "Solution found!"
            return x

        succ = generate_all_successors(x, board, goalPos)
        print "len(succ):", len(succ)
        updateStates(succ, states)

        for s in succ:
            # TODO: If node S* has previously been created, and if state(S*) = state(S), then S ← S*.
            if s.state in states:
                print "Node:", s
                print "is in states"
                s = states[s.state]
            x.kids.append(s)
            if s not in closedNodes and s not in openNodes:
                print "Not in list"
                attach_and_eval(s, x, goalPos)
                heappush(openNodes, s)
            elif x.gValue + MOVEMENT_COST < s.gValue:
                print "Elif"
                attach_and_eval(s, x, goalPos)
                if s in closedNodes:
                    propagate_path_improvements(s)


MOVEMENT_COST = 0.5

board_test = Board(generateBoard(6, 6, 1, 0, 5, 5, [[3, 2, 2, 2], [0, 3, 1, 3], [2, 0, 4, 2], [2, 5, 2, 1]]),
                   (1, 0), (5, 5))
board_0 = Board(generateBoard(10, 10, 0, 0, 9, 9, [[2, 3, 5, 5], [8, 8, 2, 1]]), (0, 0), (9, 9))

board_1 = Board(generateBoard(20, 20, 19, 3, 2, 18, [[5, 5, 10, 10], [1, 2, 4, 1]]),
                (19, 3), (2, 18))

board_2 = Board(
    generateBoard(20, 20, 0, 0, 19, 19, [[17, 10, 2, 1], [14, 4, 5, 2], [3, 16, 10, 2], [13, 7, 5, 3], [15, 15, 3, 3]]),
    (0, 0), (19, 19))

board_3 = Board(generateBoard(10, 10, 0, 0, 9, 5, [[3, 0, 2, 7], [6, 0, 4, 4], [6, 6, 2, 4]]), (0, 0), (9, 5))

board_4 = Board(generateBoard(10, 10, 0, 0, 9, 9, [[3, 0, 2, 7], [6, 0, 4, 4], [6, 6, 2, 4]]), (0, 0), (9, 9))

board_5 = Board(generateBoard(20, 20, 0, 0, 19, 13, [[4, 0, 4, 16], [12, 4, 2, 16], [16, 8, 4, 4]]),
                (0, 0), (19, 13))


def run(board):
    initiate(board.boardMatrix)
    startNode = Node(None, calculateGValue(None), calculateHValue(board.startXY[0], board.startXY[1], board.goalXY),
                     board.startXY[0], board.startXY[1])
    x = best_first_search(startNode, board.goalXY, board.boardMatrix)
    drawBoard(x, board.boardMatrix, True)


run(board_4)


# Tests
def generateSuccTest():
    testBoard = [['O' for x in range(5)] for x in range(5)]
    testBoard[0][0] = '#'
    succ = generate_all_successors(Node(Node(None, 0, 0, 1, 1), 0, 0, 1, 0),
                                   testBoard,
                                   (1, 1))
    print "Length of succ:"
    print len(succ)


def NodeSortTest():
    nodeHeap = []
    n1 = Node(None, 0, 0, 1, 0)
    n2 = Node(None, 1, 0, 2, 0)
    n3 = Node(None, 1, 1, 3, 0)
    n4 = Node(None, 0, 3, 4, 0)
    heappush(nodeHeap, n3)
    heappush(nodeHeap, n1)
    heappush(nodeHeap, n4)
    heappush(nodeHeap, n2)

    n1.set_gValue(10)
    nodeHeap.sort()

    print (heappop(nodeHeap))
    print (heappop(nodeHeap))
    print (heappop(nodeHeap))
    print (heappop(nodeHeap))

# generateSuccTest()
# NodeSortTest()
