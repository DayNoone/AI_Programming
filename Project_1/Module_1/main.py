# coding=utf-8
import math
from heapq import heappush, heappop
from Node import Node

MOVEMENT_COST = 1


def calculateHValue(initNode, goalNode):
    xOff = math.fabs(goalNode.X - initNode.X)
    yOff = math.fabs(goalNode.Y - initNode.Y)
    return xOff + yOff


def calculateGValue(initNode):
    if initNode.parent is None:
        return 0
    return initNode.parent.g + MOVEMENT_COST


def generate_all_successors(x):
    pass


def best_first_search(initNode, goalNode, ):
    closedNodes = []
    openNodes = []
    initNode.set_g(calculateGValue(initNode))
    initNode.h = calculateHValue(initNode, goalNode)

    heappush(openNodes, initNode)

    while (True):
        if openNodes.count() == 0:
            print "No solution found"
            break
        x = heappop(openNodes)
        heappush(closedNodes, x)
        if x.X == goalNode.X and x.X == goalNode.Y:
            print "Solution found!"
            break

        succ = generate_all_successors(x)

        for s in succ:
            # If node S* has previously been created, and if state(S*) = state(S), then S ← S*.
            x.kids.append(s)

