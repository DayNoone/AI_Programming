from ioHandler import *


def main():
	board, x_dimension, y_dimension, row_specs, column_specs = readBoard(1)
	print(x_dimension, y_dimension, row_specs, column_specs)
	initiate(board)
	# draw_board(board, True)

	variables = createVariables(x_dimension, y_dimension, row_specs, column_specs)


main()


def createVariables(x_dimension, y_dimension, row_specs, column_specs):
	variables = []
	for row_spec in row_specs:
		print row_spec
		numberOfValues = len(row_spec)
		sumOfValues = sum(row_spec)
		print "numberOfValues:", numberOfValues
		print "sumOfValues:", sumOfValues
	# Rfor value in row_spec:

	return variables
