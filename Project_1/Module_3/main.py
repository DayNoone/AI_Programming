from ioHandler import *

def main():
	board, x_dimension, y_dimension, row_specs, column_specs = readBoard(1)
	initiate(board)
	draw_board(board, True)


main()