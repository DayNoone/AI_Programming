from Tkinter import Tk
import copy
import random
from node import Node, initBoard
from visuals import GameWindow


def getTwoOrFour():
	if random.random() <= 0.9:
		return 1
	return 2


def generateRandomPlacementScore(board, depth):
	score = 0
	for index in range(len(board)):
		if board[index] == 0:
			value = getTwoOrFour()
			newBoard = copy.deepcopy(board)
			newBoard[index] = value
			newNode = Node(newBoard)

			if depth != 0:
				for node in makeMove(newNode.board):
					score += generateRandomPlacementScore(node.board, depth - 1)
			else:
				newNode.createHeuristic(depth)
				score += newNode.heuristic * (0.9 if value == 1 else 0.1)

	return score


def makeMove(board):
	movedLeftNode = Node(copy.deepcopy(board))
	movedLeftNode.moveLeft()

	movedRightNode = Node(copy.deepcopy(board))
	movedRightNode.moveRight()

	movedUpNode = Node(copy.deepcopy(board))
	movedUpNode.moveUp()

	movedDownNode = Node(copy.deepcopy(board))
	movedDownNode.moveDown()

	return [movedLeftNode, movedRightNode, movedUpNode, movedDownNode]


def findBestMove(node):
	listOfNodes = makeMove(node)
	boardWithHighestScore = listOfNodes[0]
	highestScore = 0
	for node in listOfNodes:
		tempScore = generateRandomPlacementScore(node.board, 2)
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
