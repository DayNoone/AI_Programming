import copy
from Project_1.genericAStarNode import AStarNode
from gui import initiate, draw_board


class Node(AStarNode):
	def __init__(self, rowVariables, columnVariables, parent, x_dimension, y_dimension):
		self.rowVariables = rowVariables
		self.columnVariables = columnVariables
		self.parent = parent
		self.x_dimension = x_dimension
		self.y_dimension = y_dimension
		AStarNode.__init__(self, parent)

	def calculateHeuristicValue(self):
		# TODO: Calculate heuristic
		# numberOfTotalDomain = 0
		# for variableId in self.rowVariables:
		# 	numberOfTotalDomain += len(self.rowVariables[variableId].domain)
		#
		# if self.checkIfContradiction():
		# 	heuristic = 999999
		# else:
		# 	heuristic = numberOfTotalDomain
		#
		# return heuristic
		return 1

	def generate_all_successors(self):
		return []
		smallestVariable = None
		smallestVariableDomainSize = 999
		for variableId in self.rowVariables:
			if 1 < len(self.rowVariables[variableId].domain) < smallestVariableDomainSize:
				smallestVariable = self.rowVariables[variableId]
				smallestVariableDomainSize = len(smallestVariable.domain)

		successors = []

		for value in smallestVariable.domain:
			variablesCopy = copy.deepcopy(self.rowVariables)
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
		for variable in self.rowVariables:
			if len(variable.domain) == 1:
				string += str(variable.type) + str(variable.position)
				for value in variable.domain[0]:
					string += str(value)
				string += "999"
		return int(string)

	# Different from Module2
	def drawBoard(self, openNodes, closedNodes, isFinished):
		board = self.generateBoard()
		draw_board(board, isFinished)

	def generateBoard(self):
		board = [[0 for column in range(self.x_dimension)] for row in range(self.y_dimension)]
		for variable in self.rowVariables:
			if len(variable.domain) == 1:
				if variable.type == 0:
					for column in range(len(variable.value)):
						board[variable.position][column] = variable.value[column]
				else:
					for row in range(len(variable.value)):
						board[row][variable.position] = variable.value[row]
		return board

	def checkIfGoalState(self):
		return False

	# for variableId in self.rowVariables:
	# 	if len(self.rowVariables[variableId].domain) != 1:
	# 		return False
	# return True

	def checkIfContradiction(self):
		return False

	# Different from Module2
	def initialFiltering(self):
		numberOfDeletedRowDomainVersions = 0
		numberOfDeletedColumnDomainVersions = 0
		for rowVariable in self.rowVariables:
			for rowVariableVersion in rowVariable.domain:

				# TODO: Find invalid rowVariableVersions

				for rowVariableDomainIndex in range(len(rowVariableVersion)):
					# For hver kolonne i raden

					isValid = False

					for columnVersion in self.columnVariables[rowVariableDomainIndex].domain:
						if columnVersion[rowVariable.position] == rowVariableVersion[rowVariableDomainIndex]:
							isValid = True
							break

					if not isValid:
						rowVariable.domain.remove(rowVariableVersion)
						numberOfDeletedRowDomainVersions += 1
						break

		for columnVariable in self.columnVariables:
			for columnVariableVersion in columnVariable.domain:

				# TODO: Find invalid rowVariableVersions

				for columnVariableDomainIndex in range(len(columnVariableVersion)):
					# For hver kolonne i raden

					isValid = False

					for rowVersion in self.rowVariables[columnVariableDomainIndex].domain:
						if rowVersion[columnVariable.position] == columnVariableVersion[columnVariableDomainIndex]:
							isValid = True
							break

					if not isValid:
						columnVariable.domain.remove(columnVariableVersion)
						numberOfDeletedColumnDomainVersions += 1
						break



		print "numberOfDeletedRowDomainVersions:", numberOfDeletedRowDomainVersions
		print "numberOfDeletedColumnDomainVersions:", numberOfDeletedColumnDomainVersions
