import copy
import random
import operator


def getTwoOrFour():
	if random.random() <= 0.9:
		return 1
	return 2


def initBoard():
	gameBoard = Node([0 for i in range(16)])
	gameBoard.placeRandomTwoOrFour()
	return gameBoard


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


class Node:
	def __init__(self, board):
		self.heuristic = 0
		self.board = board

	def setBoard(self, param):
		self.board = param

	def restartGame(self):
		self.board = [0 for i in range(16)]
		self.placeRandomTwoOrFour()

	def moveDown(self):
		lines = [[12, 8, 4, 0],
		         [13, 9, 5, 1],
		         [14, 10, 6, 2],
		         [15, 11, 7, 3]]
		self.mergeLines(lines)

	def moveUp(self):
		lines = [[0, 4, 8, 12],
		         [1, 5, 9, 13],
		         [2, 6, 10, 14],
		         [3, 7, 11, 15]]
		self.mergeLines(lines)

	def moveRight(self):
		lines = [[3, 2, 1, 0],
		         [7, 6, 5, 4],
		         [11, 10, 9, 8],
		         [15, 14, 13, 12]]

		self.mergeLines(lines)

	def moveLeft(self):
		lines = [[0, 1, 2, 3],
		         [4, 5, 6, 7],
		         [8, 9, 10, 11],
		         [12, 13, 14, 15]]

		self.mergeLines(lines)

	def mergeLines(self, lines):
		for line in lines:
			numbers = []
			for index in line:
				numbers.append(self.board[index])

			mergeResult = mergeLine(numbers)

			for index in range(len(line)):
				self.board[line[index]] = mergeResult[index]

	def isGameOver(self):
		emptySpaces = []
		for i in range(len(self.board)):
			if self.board[i] == 0:
				emptySpaces.append(i)

		if len(emptySpaces) != 0:
			return False

		else:
			left = Node(copy.deepcopy(self.board))
			left.moveLeft()
			right = Node(copy.deepcopy(self.board))
			right.moveRight()
			up = Node(copy.deepcopy(self.board))
			up.moveUp()
			down = Node(copy.deepcopy(self.board))
			down.moveDown()

			if self.board == left.board and self.board == right.board and self.board == up.board and self.board == down.board:
				return True
			else:
				return False

	def placeRandomTwoOrFour(self):
		emptySpaces = []
		for i in range(len(self.board)):
			if self.board[i] == 0:
				emptySpaces.append(i)

		if len(emptySpaces) == 0:
			return

		randomIndex = random.choice(emptySpaces)

		self.board[randomIndex] = getTwoOrFour()

	def calculateHeuristic(self):
		board = self.board

		if self.isGameOver():
			self.heuristic = -10000000000
			return

		index, value = max(enumerate(self.board), key=operator.itemgetter(1))
		# emptyspaces = 0
		# for number in self.board:
		# 	if number == 0:
		# 		emptyspaces += 1
		#
		# self.heuristic += emptyspaces * 10

		# multipliers = [15, 5, 5, 15,
		#                5, 1, 1, 5,
		#                5, 1, 1, 5,
		#                15, 5, 5, 15]

		# multipliers = [7, 6, 5, 4,
		#                6, 5, 4, 3,
		#                5, 4, 3, 2,
		#                4, 3, 2, 1]

		multipliers = [7, 6, 5, 4,
		               6, 5, 4, 3,
		               5, 4, 3, 2,
		               4, 3, 2, 1]

		for i in range(len(board)):
			if board[i] != 0:
				self.heuristic += multipliers[i] * 2**board[i]

		# if index == 0:
		# 	diagoalOfHighest = []
		# 	nextToHighest = []
		# 	lowValueOffsets = [-5, -3, 3, 5]
		# 	highValueOffset = [-4, -1, 1, 4]
		#
		# 	for offset in lowValueOffsets:
		# 		if 0 < index + offset < len(board):
		# 			diagoalOfHighest.append(index + offset)
		#
		# 	for offset in highValueOffset:
		# 		if 0 < index + offset < len(board):
		# 			nextToHighest.append(index + offset)
		#
		# 	for index in diagoalOfHighest:
		# 		self.heuristic += 3 * board[index]
		#
		# 	for index in nextToHighest:
		# 		self.heuristic += 5 * board[index]


		print "Maxvalue: ", 2 ** value, "\t Heuristic: ", self.heuristic, "\tindex: ", index


"""
Board indices:

0  1  2  3
4  5  6  7
8  9  10 11
12 13 14 15
"""
