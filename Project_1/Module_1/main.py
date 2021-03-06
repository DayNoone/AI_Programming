# coding=utf-8
from module1Node import Module1Node, Module1NinjaNode
from Project_1.genericAstar import searchAlgorithm, findLengthSolution
from generateBoard import getBoardExampleList, getBoardInfoFromInput, getBoardFromFile
from gui import drawBoard, initiate


def run(board, algorithm, heuristic, ninjaMode):
	initiate(board.boardMatrix)

	initNode = Module1Node(None, 0, 0, board.startXY[0], board.startXY[1], board, heuristic, ninjaMode)
	if ninjaMode:
		initNode = Module1NinjaNode(None, 0, 0, board.startXY[0], board.startXY[1], board, heuristic, ninjaMode)

	x, openNodes, closedNodes = searchAlgorithm(algorithm, initNode)

	if x.xPos == board.goalXY[0] or x.yPos == board.goalXY[1]:
		print
		print "Results:"
		print "\tLength of solution:\t", findLengthSolution(x, 0)
		print "\tSearched nodes:\t\t", len(openNodes) + len(closedNodes)
		print "\t\tOpen nodes:\t\t", len(openNodes)
		print "\t\tClosed nodes:\t", len(closedNodes)

	drawBoard(x, board.boardMatrix, board.startXY, board.goalXY, openNodes, closedNodes, True)


def inputValidation(inputText):
	while True:
		try:
			return int(raw_input(inputText))
		except ValueError:
			print('Please enter an integer...')


def main():
	boardList = getBoardExampleList()

	board = inputValidation('Choose board (0-5) (8 - custom, 9 - from file): ')

	if board == 8:
		selectedBoard = getBoardInfoFromInput()
	elif board == 9:
		boardFile = inputValidation('Choose board from file with int')
		selectedBoard = getBoardFromFile(boardFile)
	else:
		selectedBoard = boardList[board]

	algorithm = inputValidation('Choose from algorithms: A* (1), Depth-first (2), Breadth-first (3): ')

	heuristic = inputValidation('Choose from heuristics: Manhattan (1), Euclidean (2), No heuristic/Dijkstra (3): ')

	node = inputValidation('Choose from nodes: Normal Node (1), Ninja Node (2): ')

	# board, algorithm, heuristic, node = 5, 1, 1, 1

	ninjaMode = False;
	if node == 2:
		ninjaMode = True

	run(selectedBoard, algorithm, heuristic, ninjaMode)

	print ""


while True:
	main()
