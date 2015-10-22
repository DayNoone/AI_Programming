from Tkinter import Tk
import copy
import random
from node import Node, initBoard
from visuals import GameWindow


def getTwoOrFour():
	if random.random() <= 0.9:
		return 1
	return 2

states = {}


def calculateMovementScoreForBoard(board, depth):
	score = 0
	leafScore = 0
	emptyCellIndices = []

	for index in range(len(board)):
		if board[index] == 0:
			emptyCellIndices.append(index)

	for index in emptyCellIndices:
		# value = getTwoOrFour()
		value = 1
		newBoard = copy.deepcopy(board)
		newBoard[index] = value
		newNode = Node(newBoard)

		if depth == 0:
			key = newNode.createNodeKey()
			if key in states.keys():
				newNode.heuristic = states[key]
			else:
				newNode.calculateHeuristic()
				states[newNode.createNodeKey()] = newNode.heuristic


			if value == 1:
				leafScore = newNode.heuristic * 0.9 * 1 / len(emptyCellIndices)
			else:
				leafScore = newNode.heuristic * 0.1 * 1 / len(emptyCellIndices)
			if leafScore > score:
				score = leafScore


		else:
			listOfMoves = makeMove(newNode.board)
			highestScore = 0
			for node in listOfMoves:
				tempScore = calculateMovementScoreForBoard(node.board, depth - 1)
				if tempScore > highestScore:
					highestScore = tempScore

			score += highestScore

	return score


def makeMove(board):
	listOfNodes = []
	movedLeftNode = Node(copy.deepcopy(board))
	movedLeftNode.moveLeft()

	if movedLeftNode.board != board:
		listOfNodes.append(movedLeftNode)

	movedRightNode = Node(copy.deepcopy(board))
	movedRightNode.moveRight()

	if movedRightNode.board != board:
		listOfNodes.append(movedRightNode)

	movedUpNode = Node(copy.deepcopy(board))
	movedUpNode.moveUp()

	if movedUpNode.board != board:
		listOfNodes.append(movedUpNode)

	movedDownNode = Node(copy.deepcopy(board))
	movedDownNode.moveDown()

	if movedDownNode.board != board:
		listOfNodes.append(movedDownNode)

	return listOfNodes


def findBestMove(board):
	listOfNodes = makeMove(board)
	boardWithHighestScore = listOfNodes[0]
	highestScore = 0

	emptyCellIndices = []
	for index in range(len(board)):
		if board[index] == 0:
			emptyCellIndices.append(index)

	for node in listOfNodes:
		if len(emptyCellIndices) > 8:
			tempScore = calculateMovementScoreForBoard(node.board, 0)
		elif len(emptyCellIndices) > 6:
			tempScore = calculateMovementScoreForBoard(node.board, 1)
		elif len(emptyCellIndices) > 4:
			tempScore = calculateMovementScoreForBoard(node.board, 1)
		elif len(emptyCellIndices) > 2:
			tempScore = calculateMovementScoreForBoard(node.board, 1)
		else:
			tempScore = calculateMovementScoreForBoard(node.board, 1)

		# tempScore = calculateMovementScoreForBoard(node.board, 2)

		if tempScore > highestScore:
			boardWithHighestScore = node
			highestScore = tempScore

	return boardWithHighestScore


def leftKey(event):
	gameBoard.moveLeft()
	gameBoard.placeRandomTwoOrFour()

	window.update_view(gameBoard.board)


def rightKey(event):
	gameBoard.moveRight()
	gameBoard.placeRandomTwoOrFour()

	window.update_view(gameBoard.board)


def upKey(event):
	gameBoard.moveUp()
	gameBoard.placeRandomTwoOrFour()

	window.update_view(gameBoard.board)


def downKey(event):
	gameBoard.moveDown()
	gameBoard.placeRandomTwoOrFour()
	window.update_view(gameBoard.board)


def keyReleased(event):
	if event.char == 'r':
		gameBoard.restartGame()
		window.update_view(gameBoard.board)
	elif event.char == 's':
		newNode = findBestMove(gameBoard.board)
		gameBoard.setBoard(newNode.board)
		gameBoard.placeRandomTwoOrFour()
		window.update_view(gameBoard.board)


def startAlgorithm(event):
	while not gameBoard.isGameOver():
		newNode = findBestMove(gameBoard.board)
		gameBoard.setBoard(newNode.board)
		gameBoard.placeRandomTwoOrFour()
		window.update_view(gameBoard.board)


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
window.update_view(gameBoard.board)  # 1D list representing the board

window.mainloop()

newNode = findBestMove([1, 8, 9, 10,
						 5, 7, 6, 4,
						 1, 4, 5, 3,
						 1, 3, 2, 1])

print newNode
