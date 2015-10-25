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


def boostClustering(board):
	extraHeuristic = 0
	highValueOffset = [-4, -1, 1, 4]
	for index in range(len(board)):
		for offset in highValueOffset:
			neighborIndex = index + offset
			if 0 < neighborIndex < len(board):
				if board[neighborIndex] == board[index]:
					extraHeuristic += 100 * 2 ** board[index]
				elif board[neighborIndex] - 1 == board[index] or board[neighborIndex] + 1 == board[index]:
					extraHeuristic += 50 * 2 ** board[index]
	return extraHeuristic


def boostSnakePattern(board):
	extraHeuristic = 0
	multipliers = [130, 140, 150, 160,
	               120, 110, 100, 90,
	               50, 60, 70, 80,
	               40, 30, 20, 10]
	for i in range(len(board)):
		if board[i] != 0:
			extraHeuristic += multipliers[i] * 2 ** board[i]
	return extraHeuristic


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

		emptyCellPoints = self.boostEmptyCells()
		self.heuristic += emptyCellPoints
		print "Empty cell points:\t", emptyCellPoints

		clusterinPoints = boostClustering(board)
		self.heuristic += clusterinPoints
		print "Clustering points:\t", clusterinPoints

		patternPoints = boostSnakePattern(board)
		self.heuristic += patternPoints
		print "Pattern points:\t\t", patternPoints

		print "Maxvalue: ", 2 ** value, "\t Heuristic: ", self.heuristic, "\tindex: ", index

	def boostEmptyCells(self):
		emptyspaces = 0
		for number in self.board:
			if number == 0:
				emptyspaces += 1
		extraHeuristic = emptyspaces * 10000
		return extraHeuristic

	def createNodeKey(self):
		nodeKey = ""
		for index in self.board:
			nodeKey = nodeKey + str(index) + "x"
		return nodeKey



"""
Board indices:

0  1  2  3
4  5  6  7
8  9  10 11
12 13 14 15
"""
