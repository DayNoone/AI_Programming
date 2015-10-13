from Tkinter import Tk
import copy
from node import Node, initBoard
from visuals import GameWindow


def generateRandomPlacementScore(board, depth):
	score = 0
	for index in range(len(board)):
		if board[index] == 0:
			for value in range(1, 3):
				newBoard = copy.deepcopy(board)
				newBoard[index] = value
				newNode = Node(newBoard)
				newNode.createHeuristic(depth)
				score = newNode.heuristic * (0.9 if value == 1 else 0.1)
	return score


def findBestMove(node):
	movedLeftNode = Node(copy.deepcopy(node))
	movedLeftNode.moveLeft()

	movedRightNode = Node(copy.deepcopy(node))
	movedRightNode.moveRight()

	movedUpNode = Node(copy.deepcopy(node))
	movedUpNode.moveUp()

	movedDownNode = Node(copy.deepcopy(node))
	movedDownNode.moveDown()

	listOfNodes = [movedLeftNode, movedRightNode, movedUpNode, movedDownNode]
	boardWithHighestScore = movedLeftNode
	highestScore = 0
	for node in listOfNodes:
		tempScore = generateRandomPlacementScore(node.board, 0)
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
