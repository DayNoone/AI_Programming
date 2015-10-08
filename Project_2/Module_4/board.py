import random


def getTwoOrFour():
	if random.random() <= 0.9:
		return 1
	return 2


def initBoard():
	board = Board([0 for i in range(16)])
	board.placeRandomTwoOrFour()
	return board


def mergeLine(line):
	nonzeros_removed = []
	result = []
	merged = False
	for number in line:
		if number != 0:
			nonzeros_removed.append(number)

	while len(nonzeros_removed) != len(line):
		nonzeros_removed.append(0)

	# Double sequental tiles if same value
	for number in range(0, len(nonzeros_removed) - 1):
		if nonzeros_removed[number] != 0 and nonzeros_removed[number] == nonzeros_removed[
					number + 1] and merged is False:
			result.append(nonzeros_removed[number] + 1)
			merged = True
		elif nonzeros_removed[number] != nonzeros_removed[number + 1] and merged is False:
			result.append(nonzeros_removed[number])
		elif merged is True:
			merged = False

	if nonzeros_removed[-1] != 0 and merged is False:
		result.append(nonzeros_removed[-1])

	while len(result) != len(nonzeros_removed):
		result.append(0)

	return result


"""
Board indices:

0  1  2  3
4  5  6  7
8  9  10 11
12 13 14 15
"""


class Board:
	def __init__(self, board):
		self.board = board

	def setBoard(self, param):
		self.board = param

	def moveDown(self):
		lines = [[12, 8, 4, 0],
		         [13, 9, 5, 1],
		         [14, 10, 6, 2],
		         [15, 11, 7, 3]]
		self.mergeLines(lines)
		self.placeRandomTwoOrFour()

	def moveUp(self):
		lines = [[0, 4, 8, 12],
		         [1, 5, 9, 13],
		         [2, 6, 10, 14],
		         [3, 7, 11, 15]]
		self.mergeLines(lines)
		self.placeRandomTwoOrFour()

	def moveRight(self):
		lines = [[3, 2, 1, 0],
		         [7, 6, 5, 4],
		         [11, 10, 9, 8],
		         [15, 14, 13, 12]]

		self.mergeLines(lines)
		self.placeRandomTwoOrFour()

	def moveLeft(self):
		lines = [[0, 1, 2, 3],
		         [4, 5, 6, 7],
		         [8, 9, 10, 11],
		         [12, 13, 14, 15]]

		self.mergeLines(lines)
		self.placeRandomTwoOrFour()

	def mergeLines(self, lines):
		for line in lines:
			numbers = []
			for index in line:
				numbers.append(self.board[index])

			mergeResult = mergeLine(numbers)

			for index in range(len(line)):
				self.board[line[index]] = mergeResult[index]

	def placeRandomTwoOrFour(self):
		emptySpaces = []
		for i in range(len(self.board)):
			if self.board[i] == 0:
				emptySpaces.append(i)

		if len(emptySpaces) == 0:
			print "GAME OVER"
			return

		randomIndex = random.choice(emptySpaces)

		self.board[randomIndex] = getTwoOrFour()
