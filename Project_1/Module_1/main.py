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
    return (xOff + yOff) * MOVEMENT_COST


def calculateGValue(parent):
    if parent is None:
        return 0
    return parent.gValue + MOVEMENT_COST


def generate_all_successors(parent, board, goalPos):
    newChildPositions = [
        (parent.xPos + 1, parent.yPos),
        (parent.xPos - 1, parent.yPos),
        (parent.xPos, parent.yPos + 1),
        (parent.xPos, parent.yPos - 1)
    ]
    newChildren = []
    for newChildPosition in newChildPositions:
        if 0 <= newChildPosition[0] < len(board) and 0 <= newChildPosition[1] < len(board):
            if board[newChildPosition[0]][newChildPosition[1]] != '#':
                if parent.parent is not None and parent.parent.xPos == newChildPosition[0] and parent.parent.yPos == \
                        newChildPosition[1]:
                    continue
                newChildren.append(Node(parent, 0, 0, newChildPosition[0], newChildPosition[1]))

    return newChildren


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
        s.state = int(str(s.xPos) + "00000" + str(s.yPos))
        if s.state not in states:
            states[s.state] = s


def best_first_search(initNode, goalPos, board, debug):
    closedNodes = []
    openNodes = []
    states = {}
    initNode.set_gValue(0)
    initNode.set_hValue(calculateHValue(initNode.xPos, initNode.yPos, goalPos))

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

        openNodes.sort()

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

        x = heappop(openNodes)

        if debug:
            print "Popped node:", x

        drawBoard(x, board, openNodes, closedNodes, False)

        heappush(closedNodes, x)
        if x.xPos == goalPos[0] and x.yPos == goalPos[1]:
            print "Solution found!"
            return x, openNodes, closedNodes

        succ = generate_all_successors(x, board, goalPos)

        if debug:
            print "len(succ):", len(succ)
            for a in succ:
                print a

        updateStates(succ, states)

        for s in succ:
            s = states[s.state]
            x.kids.append(s)
            if s not in closedNodes and s not in openNodes:
                if debug:
                    print "Not in any list"

                attach_and_eval(s, x, goalPos)
                heappush(openNodes, s)

            elif x.gValue + MOVEMENT_COST < s.gValue:
                if debug:
                    print "Elif"

                attach_and_eval(s, x, goalPos)
                if s in closedNodes:
                    propagate_path_improvements(s)


MOVEMENT_COST = 1

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

scenarioWeird = Board(generateBoard(20, 20, 0, 0, 19, 19, [[1, 18, 18, 1], [18, 1, 1, 18]]), (0, 0), (19, 19))


def run(board):
    initiate(board.boardMatrix)
    startNode = Node(None, calculateGValue(None), calculateHValue(board.startXY[0], board.startXY[1], board.goalXY),
                     board.startXY[0], board.startXY[1])
    x, openNodes, closedNodes = best_first_search(startNode, board.goalXY, board.boardMatrix, True)
    drawBoard(x, board.boardMatrix, openNodes, closedNodes, True)

def main():
    board = int(raw_input('Choose board (1-5): '))
    boardList = [board_0, board_1, board_2, board_3, board_4, board_5]

    algorithm = int(raw_input('Choose from algorithms: A* (1), Best-first (2), Depth-first (3), Breadth-first (4): '))

    run(boardList[board])

main()