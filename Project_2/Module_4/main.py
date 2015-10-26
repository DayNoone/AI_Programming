from Tkinter import Tk
import copy
import random
import time
from node import initBoard, isGameOver, placeRandomTwoOrFour, moveLeft, moveRight, moveUp, moveDown, calculateHeuristic, \
	restartGame
from visuals import GameWindow


def getTwoOrFour():
	if random.random() <= 0.9:
		return 1
	return 2


def maxValue(board, depth):
	listOfMoves = makeMove(board)
	highestScore = 0
	for tempBoard in listOfMoves:
		tempScore = calculateMovementScoreForBoard(tempBoard, depth - 1)
		if tempScore > highestScore:
			highestScore = tempScore
	return highestScore


def expValue(board, depth):
	score = 0
	emptyCellIndices = []

	for index in range(len(board)):
		if board[index] == 0:
			emptyCellIndices.append(index)

	for index in emptyCellIndices:
		for value in range(1, 2):
			newBoard = copy.deepcopy(board)
			newBoard[index] = value

			if value == 1:
				p = 0.9 * 1.0 / len(emptyCellIndices)
			else:
				p = 0.1 * 1.0 / len(emptyCellIndices)

			score += p * calculateMovementScoreForBoard(newBoard, depth - 1)

	return score


def calculateMovementScoreForBoard(board, depth):
	tempBoard = copy.deepcopy(board)

	if depth == 0:
		heuristic = calculateHeuristic(tempBoard)
		return heuristic

	elif depth % 2 == 0:
		return maxValue(tempBoard, depth)

	else:
		return expValue(tempBoard, depth)


def makeMove(board):
	listOfBoards = []
	movedLeft = copy.deepcopy(board)
	moveLeft(movedLeft)

	if movedLeft != board:
		listOfBoards.append(movedLeft)

	movedRight = copy.deepcopy(board)
	moveRight(movedRight)

	if movedRight != board:
		listOfBoards.append(movedRight)

	movedUp = copy.deepcopy(board)
	moveUp(movedUp)

	if movedUp != board:
		listOfBoards.append(movedUp)

	movedDown = copy.deepcopy(board)
	moveDown(movedDown)

	if movedDown != board:
		listOfBoards.append(movedDown)

	return listOfBoards


def findBestMove(board):
	listOfBoards = makeMove(board)
	boardWithHighestScore = listOfBoards[0]
	highestScore = 0

	emptyCellIndices = []
	for index in range(len(board)):
		if board[index] == 0:
			emptyCellIndices.append(index)

	for board in listOfBoards:
		if len(emptyCellIndices) > 8:
			tempScore = calculateMovementScoreForBoard(board, 1)
		elif len(emptyCellIndices) > 6:
			tempScore = calculateMovementScoreForBoard(board, 3)
		elif len(emptyCellIndices) > 4:
			tempScore = calculateMovementScoreForBoard(board, 5)
		elif len(emptyCellIndices) > 2:
			tempScore = calculateMovementScoreForBoard(board, 5)
		else:
			tempScore = calculateMovementScoreForBoard(board, 7)

		# tempScore = calculateMovementScoreForBoard(board, 5)
		if tempScore > highestScore:
			boardWithHighestScore = board
			highestScore = tempScore
	return boardWithHighestScore


def leftKey(event):
	moveLeft(gameBoard)
	placeRandomTwoOrFour(gameBoard)

	window.update_view(gameBoard)


def rightKey(event):
	moveRight(gameBoard)
	placeRandomTwoOrFour(gameBoard)

	window.update_view(gameBoard)


def upKey(event):
	moveUp(gameBoard)
	placeRandomTwoOrFour(gameBoard)

	window.update_view(gameBoard)


def downKey(event):
	moveDown(gameBoard)
	placeRandomTwoOrFour(gameBoard)
	window.update_view(gameBoard)


def keyReleased(event):
	if event.char == 'r':
		restartGame(gameBoard)
		window.update_view(gameBoard)
	elif event.char == 's':
		newNode = findBestMove(gameBoard)
		gameBoard = newNode
		placeRandomTwoOrFour(gameBoard)
		window.update_view(gameBoard.board)


def gamewon(board):
	for number in board:
		if number >= 11:
			return True
	return False


def startAlgorithm(event):
	board = initBoard()

	alreadyCompleted = False
	startTime = time.time()
	while not isGameOver(board):
		bestBoard = findBestMove(board)
		if not alreadyCompleted and gamewon(bestBoard):
			gameWonTime = time.time()
			gametime = gameWonTime - startTime
			print "######"
			print "YOU WON! Time elapsed:", gametime / 60.0, " minutes - WITHOUT NODE"
			print "######"
			print ""
			alreadyCompleted = True
		board = bestBoard
		placeRandomTwoOrFour(board)
		window.update_view(board)


main = Tk()

window = GameWindow(main)

main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
main.bind('<Up>', upKey)
main.bind('<Down>', downKey)
main.bind('<KeyRelease>', keyReleased)
main.bind('<space>', startAlgorithm)

window.pack()

gameBoard = initBoard()
window.update_view(gameBoard)  # 1D list representing the board

window.mainloop()
