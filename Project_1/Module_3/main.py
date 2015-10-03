import copy
from node import Node
from Project_1.genericAstar import searchAlgorithm
from variable import Variable
from ioHandler import *


def calculateSumOfRest(row_spec, i):
	sum = 0
	for pos in range(i + 1, len(row_spec)):
		sum += row_spec[pos]
	return sum


def calculateNumberOfRest(row_spec, i):
	count = 0
	for pos in range(i + 1, len(row_spec)):
		count += 1
	return count


def insertPossibilities(alternative, row_spec, i, domain):
	restCount = calculateNumberOfRest(row_spec, i)
	sumOfRest = calculateSumOfRest(row_spec, i)

	nextEarliestStart = 0

	for pos in range(len(alternative) - 1, -1, -1):
		if alternative[pos] == 1:
			nextEarliestStart = pos + 2
			break;

	try:
		row_spec[i]
	except:
		print "OMG"

	rightMostPosition = len(alternative) - restCount - sumOfRest - row_spec[i]

	for posInAlternative in range(nextEarliestStart, rightMostPosition + 1):
		newAlternative = copy.deepcopy(alternative)
		for fillIndex in range(posInAlternative, posInAlternative + row_spec[i]):
			newAlternative[fillIndex] = 1
		if len(row_spec) - 1 == i:
			domain.append(newAlternative)
		else:
			insertPossibilities(newAlternative, row_spec, i + 1, domain)


def generateVariables(specs, dimension, rowOrColumn):
	variables = {}
	for row_specIndex in range(len(specs)):
		domain = []
		variable = Variable(rowOrColumn, row_specIndex, domain)

		emptyAlternative = [0 for i in range(dimension)]

		insertPossibilities(emptyAlternative, specs[row_specIndex], 0, domain)

		variables[variable.position] = variable

		if len(variable.domain) == 1:
			variable.value = variable.domain[0]

	return variables


def main():
	board, x_dimension, y_dimension, row_specs, column_specs = readBoard(1)
	initiate(board)
	# draw_board(board, True)

	rowVars = generateVariables(row_specs, x_dimension, 0)
	colVars = generateVariables(column_specs, y_dimension, 1)

	initNode = Node(rowVars, colVars, None, x_dimension, y_dimension)

	if not initNode.checkIfGoalState() and not initNode.checkIfContradiction():
		initNode.initialFiltering()
		x, opennodes, closednodes = searchAlgorithm(1, initNode, False)
		x.drawBoard(opennodes, closednodes, True)


main()
