from ioHandler import *

def main():
	board, x_dimension, y_dimension, row_specs, column_specs = readBoard(1)
	print(x_dimension, y_dimension, row_specs, column_specs)
	initiate(board)
	draw_board(board, True)

	createVariables(x_dimension, y_dimension, row_specs, column_specs)


main()

def createVariables():
	pass