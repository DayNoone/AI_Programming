from Project_1.genericAStarNode import AStarNode
from gui import initiate, draw_board

class Node(AStarNode):
	def __init__(self, variables, parent, x_dimension, y_dimension):
		self.variables = variables
		self.parent = parent
		self.x_dimension = x_dimension
		self.y_dimension = y_dimension

	def calculateHeuristicValue(self):
		pass

	def generate_all_successors(self):
		pass

	def calculateGValue(self):
		pass

	def calculateStateIndex(self):
		pass

	def drawBoard(self, openNodes, closedNodes, isFinished):
		board = self.generateBoard()
		draw_board(board)

	def generateBoard(self):
		board = [[0 for column in range(self.x_dimension)] for row in range(self.y_dimension)]
		for variable in self.variables:
			if len(variable.domain) == 1:
				if variable.type == 0:
					for column in range(len(variable.value)):
						board[variable.position][column] = variable.value[column]
				else:
					for row in range(len(variable.value)):
						board[row][variable.position] = variable.value[row]
		return board

	def checkIfGoalState(self):
		pass