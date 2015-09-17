from ioHandler import *
from Node2 import Node
import os

# General outline of Algorithm

# Generate initial state S0, in which each variable has its full domain
# Refine S0 by running GAC-Initialize and then GAC-Domain-Filtering-Loop
# If S0 is neither a solution nor a contradictory state, then:
#   Continue normal A* search (with S0 in the root node) by:
#       Popping search nodes from the agenda
#       Generating their successor states (by makin assumptions)
#       Enforcing the assumption in each successor state by reducing the domain of the assumed variable to a singleton set
#       Calling GAC-Rerun on each newly-generated state
#       Computing the f, g and h values for each new state,
#           where h i based on the state of the CSP after the call to GAC-Rerun

def makefunc(var_names, expression, envir=globals()):
    #---------makefunc(['x','y','z'], 'x + y < 2*z or x < y')
    args = ""
    for n in var_names:
        args = args + ", " + n
    return eval("(lambda " + args[1:] + ": " + expression + ")", envir)


def main():
    board = inputValidation('Choose board (0-5): ')
    k = inputValidation('Choose domain size: ')
    graph = readBoard(boards[board])
    initiate(graph)
    variables = create_Variables(graph, [x for x in range(k)])
    draw_board(variables, graph, False)

    s0 = Node(variables, [x for x in range(k)])
    draw_board(variables, graph, True)



main()
