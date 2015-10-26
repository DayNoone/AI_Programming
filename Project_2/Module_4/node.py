import copy
import random
import operator


def getTwoOrFour():
	if random.random() <= 0.9:
		return 1
	return 2


def initBoard():
	gameBoard = [0 for i in range(16)]
	placeRandomTwoOrFour(gameBoard)
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
					extraHeuristic += 50.0 * 2 ** board[index]
				elif board[neighborIndex] - 1 == board[index] or board[neighborIndex] + 1 == board[index]:
					extraHeuristic += 10.0 * 2 ** board[index]
	return extraHeuristic


def boostSnakePattern(board, highestValueIndex, secondHighestValueIndex):
	if highestValueIndex == 1:
		multipliers = [16, 15, 14, 13,
		               9, 10, 11, 12,
		               8, 7, 6, 5,
		               1, 2, 3, 4]
	elif highestValueIndex == 4:
		multipliers = [16, 9, 8, 1,
		               15, 10, 7, 2,
		               14, 11, 6, 3,
		               13, 12, 5, 4]
	elif highestValueIndex == 0 or highestValueIndex == 5:
		if secondHighestValueIndex == 1:
			multipliers = [16, 15, 14, 13,
			               9, 10, 11, 12,
			               8, 7, 6, 5,
			               1, 2, 3, 4]
		elif secondHighestValueIndex == 4:
			multipliers = [16, 9, 8, 1,
			               15, 10, 7, 2,
			               14, 11, 6, 3,
			               13, 12, 5, 4]
		else:
			multipliers = [16, 15, 14, 13,
			               9, 10, 11, 12,
			               8, 7, 6, 5,
			               1, 2, 3, 4]

	elif highestValueIndex == 2:
		multipliers = [13, 14, 15, 16,
		               12, 11, 10, 9,
		               5, 6, 7, 8,
		               4, 3, 2, 1]
	elif highestValueIndex == 6:
		multipliers = [4, 8, 9, 16,
		               3, 7, 10, 15,
		               2, 6, 11, 14,
		               1, 5, 12, 13]
	elif highestValueIndex == 3 or highestValueIndex == 7:
		if secondHighestValueIndex == 2:
			multipliers = [13, 14, 15, 16,
			               12, 11, 10, 9,
			               5, 6, 7, 8,
			               4, 3, 2, 1]
		elif secondHighestValueIndex == 6:
			multipliers = [4, 8, 9, 16,
			               3, 7, 10, 15,
			               2, 6, 11, 14,
			               1, 5, 12, 13]
		else:
			multipliers = [13, 14, 15, 16,
			               12, 11, 10, 9,
			               5, 6, 7, 8,
			               4, 3, 2, 1]

	elif highestValueIndex == 8:
		multipliers = [13, 12, 8, 1,
		               14, 11, 7, 2,
		               15, 10, 6, 3,
		               16, 9, 5, 4]
	elif highestValueIndex == 13:
		multipliers = [1, 2, 3, 4,
		               8, 7, 6, 5,
		               9, 10, 11, 12,
		               16, 15, 14, 13]
	elif highestValueIndex == 9 or highestValueIndex == 12:
		if secondHighestValueIndex == 8:
			multipliers = [13, 12, 8, 1,
			               14, 11, 7, 2,
			               15, 10, 6, 3,
			               16, 9, 5, 4]
		elif secondHighestValueIndex == 13:
			multipliers = [1, 2, 3, 4,
			               8, 7, 6, 5,
			               9, 10, 11, 12,
			               16, 15, 14, 13]
		else:
			multipliers = [13, 12, 8, 1,
			               14, 11, 7, 2,
			               15, 10, 6, 3,
			               16, 9, 5, 4]

	elif highestValueIndex == 11:
		multipliers = [4, 5, 12, 13,
		               3, 6, 11, 14,
		               2, 7, 10, 15,
		               1, 8, 9, 16]
	elif highestValueIndex == 14:
		multipliers = [4, 3, 2, 1,
		               5, 6, 7, 8,
		               12, 11, 10, 9,
		               13, 14, 15, 16]
	# elif highestValueIndex == 10 or highestValueIndex == 15:
	else:
		if secondHighestValueIndex == 11:
			multipliers = [4, 5, 12, 13,
			               3, 6, 11, 14,
			               2, 7, 10, 15,
			               1, 8, 9, 16]
		elif secondHighestValueIndex == 14:
			multipliers = [4, 3, 2, 1,
			               5, 6, 7, 8,
			               12, 11, 10, 9,
			               13, 14, 15, 16]
		else:
			multipliers = [4, 5, 12, 13,
			               3, 6, 11, 14,
			               2, 7, 10, 15,
			               1, 8, 9, 16]

	extraHeuristic = 0
	for i in range(len(board)):
		if board[i] != 0:
			extraHeuristic += multipliers[i] * 10 * 2 ** board[i]

	return extraHeuristic


def restartGame():
	board = [0 for i in range(16)]
	placeRandomTwoOrFour(board)
	return board


def moveDown(board):
	lines = [[12, 8, 4, 0],
	         [13, 9, 5, 1],
	         [14, 10, 6, 2],
	         [15, 11, 7, 3]]
	mergeLines(board, lines)


def moveUp(board):
	lines = [[0, 4, 8, 12],
	         [1, 5, 9, 13],
	         [2, 6, 10, 14],
	         [3, 7, 11, 15]]
	mergeLines(board, lines)


def moveRight(board):
	lines = [[3, 2, 1, 0],
	         [7, 6, 5, 4],
	         [11, 10, 9, 8],
	         [15, 14, 13, 12]]

	mergeLines(board, lines)


def moveLeft(board):
	lines = [[0, 1, 2, 3],
	         [4, 5, 6, 7],
	         [8, 9, 10, 11],
	         [12, 13, 14, 15]]

	mergeLines(board, lines)


def mergeLines(board, lines):
	for line in lines:
		numbers = []
		for index in line:
			numbers.append(board[index])

		mergeResult = mergeLine(numbers)

		for index in range(len(line)):
			board[line[index]] = mergeResult[index]


def isGameOver(board):
	emptySpaces = []
	for i in range(len(board)):
		if board[i] == 0:
			emptySpaces.append(i)

	if len(emptySpaces) != 0:
		return False

	else:
		left = copy.deepcopy(board)
		moveLeft(left)
		right = copy.deepcopy(board)
		moveRight(right)
		up = copy.deepcopy(board)
		moveUp(up)
		down = copy.deepcopy(board)
		moveDown(down)

		if board == left and board == right and board == up and board == down:
			return True
		else:
			return False


def placeRandomTwoOrFour(board):
	emptySpaces = []
	for i in range(len(board)):
		if board[i] == 0:
			emptySpaces.append(i)

	if len(emptySpaces) == 0:
		return

	randomIndex = random.choice(emptySpaces)

	board[randomIndex] = getTwoOrFour()


def calculateHeuristic(board):
	heuristic = 0
	if isGameOver(board):
		return -10000000000

	highestValueIndex = 0
	secondHighestValueIndex = 0
	for index in range(len(board)):
		tempValue = board[index]
		if tempValue > highestValueIndex:
			secondHighestValueIndex = highestValueIndex
			highestValueIndex = tempValue
		elif tempValue > secondHighestValueIndex:
			secondHighestValueIndex = tempValue

	emptyCellPoints = boostEmptyCells(board)
	heuristic += emptyCellPoints
	# print "Empty cell points:\t", emptyCellPoints

	clusteringPoints = boostClustering(board)
	heuristic += clusteringPoints
	# print "Clustering points:\t", clusterinPoints

	patternPoints = boostSnakePattern(board, highestValueIndex, secondHighestValueIndex)
	heuristic += patternPoints
	# print "Pattern points:\t\t", patternPoints

	return heuristic


# print "Maxvalue: ", 2 ** value, "\t Heuristic: ", self.heuristic, "\tindex: ", index

def boostEmptyCells(board):
	emptyspaces = 0
	for number in board:
		if number == 0:
			emptyspaces += 1
	extraHeuristic = emptyspaces * 10000.0
	return extraHeuristic
