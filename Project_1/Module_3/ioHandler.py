from gui import initiate, draw_board
import os

boards = ['nono1.txt', 'nono2.txt', 'nono3.txt', 'nono4.txt', 'nono5.txt']

# boards = ['nono-camel.txt', 'nono-cat.txt', 'nono-chick.txt', 'nono-heart-1.txt', 'nono-rabbit.txt', 'nono-sailboat.txt', 'nono-telephone.txt', 'nono-hard.txt', 'nono-multiple.txt', 'nono-ship.txt']


def readFile(path):
	row_specs = []
	column_specs = []
	with open(path) as f:
		x_dimension, y_dimension = [int(x) for x in f.readline().split()]  # read first line
		for row in range(y_dimension):
			line = f.readline().strip().split(' ')
			line = map(int, line)
			row_specs.append(line)
		for column in range(x_dimension):
			line = f.readline().strip().split(' ')
			line = map(int, line)
			column_specs.append(line)
		row_specs = row_specs[::-1]
	board = [[0 for y in range(x_dimension)] for x in range(y_dimension)]
	return board, x_dimension, y_dimension, row_specs, column_specs


def readBoard(no):
	if os.name == 'nt':
		return readFile('scenarios\\' + boards[no])
	else:
		return readFile('scenarios/' + boards[no])


def inputValidation(inputText):
	while True:
		try:
			return int(raw_input(inputText))
		except ValueError:
			print('Please enter an integer...')
