import copy
from Project_1.genericAStarNode import AStarNode
from gui import initiate, draw_board

class Node(AStarNode):
	def __init__(self, variables, parent, x_dimension, y_dimension):
		self.variables = variables
		self.parent = parent
		self.x_dimension = x_dimension
		self.y_dimension = y_dimension

	def calculateHeuristicValue(self):
		numberOfTotalDomain = 0
		for variableId in self.variables:
			numberOfTotalDomain += len(self.variables[variableId].domain)

		if self.checkIfContradiction():
			heuristic = 999999
		else:
			heuristic = numberOfTotalDomain

		return heuristic

	def generate_all_successors(self):
		smallestVariable = None
		smallestVariableDomainSize = 999
		for variableId in self.variables:
			if 1 < len(self.variables[variableId].domain) < smallestVariableDomainSize:
				smallestVariable = self.variables[variableId]
				smallestVariableDomainSize = len(smallestVariable.domain)

		successors = []

		for value in smallestVariable.domain:
			variablesCopy = copy.deepcopy(self.variables)
			variable = variablesCopy[smallestVariable.id]
			variable.colorid = value
			variable.domain = [value]
			newNode = Node(variablesCopy, self)
			newNode.revise(variable)

			successors.append(newNode)

		return successors

	def calculateGValue(self):
		if self.parent is None:
			return 0
		return self.parent.gValue + self.MOVEMENT_COST

	# Different from Module2
	def calculateStateIndex(self):
		string = "0"
		for variable in self.variables:
			if len(variable.domain) == 1:
				string += str(variable.type) + str(variable.position)
				for value in variable.domain[0]:
					string += str(value)
				string += "999"
		return int(string)

	# Different from Module2
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
		for variableId in self.variables:
			if len(self.variables[variableId].domain) != 1:
				return False
		return True

	# Different from Module2
	def revise(self):
		pass