import sys
from ioHandler import *
from node import Node
from Project_1.genericAstar import searchAlgorithm, findLengthSolution


def makefunc(var_names, expression, envir=globals()):
	# ---------makefunc(['x','y','z'], 'x + y < 2*z or x < y')
	args = ""
	for n in var_names:
		args = args + ", " + n
	return eval("(lambda " + args[1:] + ": " + expression + ")", envir)


def getCountUsatConstraints(node):
	count = 0
	for variableid, variable in node.variables.iteritems():
		if variable.colorid is not None:
			for neigborID in variable.constraints[variableid]:
				if variable.colorid == node.variables[neigborID].colorid:
					count += 1

	return count / 2


def getNumNonColoredVars(node):
	count = 0
	for variableid, variable in node.variables.iteritems():
		if variable.colorid is None:
			count += 1

	return count



def main():
	sys.setrecursionlimit(10000)
	boardNo = inputValidation('Choose board (0-5): ')
	k = inputValidation('Choose domain size: ')
	graph = readBoard(boards[boardNo])
	initiate(graph)
	variables = create_Variables(graph, k)

	node = Node(variables, None)

	if not node.checkIfGoalState() and not node.checkIfContradiction():
		x, opennodes, closednodes = searchAlgorithm(1, node)
		numberOfUnsatisfiedConstraints = getCountUsatConstraints(x)
		numNonColoredVars = getNumNonColoredVars(x)
		print "Number of unsatisfied constraints:\t\t", numberOfUnsatisfiedConstraints
		print "Number of variables without color:\t\t", numNonColoredVars
		print "Nodes in the search tree:\t\t\t\t", len(opennodes) + len(closednodes)
		print "Number of nodes popped and expanded:\t", len(closednodes)
		print "Length of path from root to solution:\t", findLengthSolution(x, 0)

		x.drawBoard(opennodes, closednodes, True)


main()

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
