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
		self.state = self.calculateStateIndex()
		AStarNode.__init__(self, parent)

	def calculateHeuristicValue(self):
		# TODO: Calculate heuristic
		numberOfTotalDomain = 0
		for variableId in self.rowVariables:
			numberOfTotalDomain += len(self.rowVariables[variableId].domain)

		for variableId in self.columnVariables:
			numberOfTotalDomain += len(self.columnVariables[variableId].domain)

		if self.checkIfContradiction():
			heuristic = 999999
		else:
			heuristic = numberOfTotalDomain

		return heuristic

	def generate_all_successors(self):
		smallestVariable = None
		# TODO: Do better! Start with domainSize of first variable?
		smallestVariableDomainSize = 999

		# TODO: Stop if domainsize == 2?? Maybe not faster
		for variableId in self.rowVariables:
			if 1 < len(self.rowVariables[variableId].domain) < smallestVariableDomainSize:
				smallestVariable = self.rowVariables[variableId]
				smallestVariableDomainSize = len(smallestVariable.domain)

		for variableId in self.columnVariables:
			if 1 < len(self.columnVariables[variableId].domain) < smallestVariableDomainSize:
				smallestVariable = self.columnVariables[variableId]
				smallestVariableDomainSize = len(smallestVariable.domain)

		successors = []

		if smallestVariable == None:
			print "asdf"

		for value in smallestVariable.domain:
			rowVariablesCopy = copy.deepcopy(self.rowVariables)
			columnVariablesCopy = copy.deepcopy(self.columnVariables)

			if smallestVariable.type == 0:
				variablesCopy = rowVariablesCopy
			else:
				variablesCopy = columnVariablesCopy

			variable = None
			for tempVariableId in variablesCopy:
				if smallestVariable.position == variablesCopy[tempVariableId].position:
					variable = variablesCopy[tempVariableId]

			variable.setValue(value)
			variable.domain = [value]
			newNode = Node(rowVariablesCopy, columnVariablesCopy, self, self.x_dimension, self.y_dimension)
			# newNode.revise(variable)
			newNode.initialFiltering()

			successors.append(newNode)

		return successors

	def calculateGValue(self):
		if self.parent is None:
			return 0
		return self.parent.gValue + self.MOVEMENT_COST

	# Different from Module2
	def calculateStateIndex(self):
		string = "0"
		for rowVariableId in self.rowVariables:
			if self.rowVariables[rowVariableId].value is not None:
				string += str(rowVariableId) + ''.join(str(i) for i in self.rowVariables[rowVariableId].value) + "999"

		for columnVariableId in self.columnVariables:
			if self.columnVariables[columnVariableId].value is not None:
				string += str(columnVariableId) + ''.join(str(i) for i in self.columnVariables[columnVariableId].value) + "999"

		return int(string)

	# Different from Module2
	def drawBoard(self, openNodes, closedNodes, isFinished):
		board = self.generateBoard()
		draw_board(board, isFinished)

	def generateBoard(self):
		board = [[0 for column in range(self.x_dimension)] for row in range(self.y_dimension)]
		for variableId in self.rowVariables:
			if len(self.rowVariables[variableId].domain) == 1:
				if self.rowVariables[variableId].type == 0:
					for column in range(len(self.rowVariables[variableId].value)):
						board[self.rowVariables[variableId].position][column] = self.rowVariables[variableId].value[column]
				else:
					for row in range(len(self.rowVariables[variableId].value)):
						board[row][self.rowVariables[variableId].position] = self.rowVariables[variableId].value[row]

		for variableId in self.columnVariables:
			if len(self.columnVariables[variableId].domain) == 1:
				if self.columnVariables[variableId].type == 0:
					for column in range(len(self.columnVariables[variableId].value)):
						board[self.columnVariables[variableId].position][column] = self.columnVariables[variableId].value[column]
				else:
					for row in range(len(self.columnVariables[variableId].value)):
						board[row][self.columnVariables[variableId].position] = self.columnVariables[variableId].value[row]

		return board

	def checkIfGoalState(self):

		for variableId in self.rowVariables:
			variable = self.rowVariables[variableId]
			if len(variable.domain) != 1:
				return False

		for variableId in self.columnVariables:
			variable = self.columnVariables[variableId]
			if len(variable.domain) != 1:
				return False

		return True

	def checkIfContradiction(self):
		for variableId in self.rowVariables:
			rowVariable = self.rowVariables[variableId]
			if len(rowVariable.domain) == 0:
				return True

		for variableId in self.columnVariables:
			columnVariable = self.columnVariables[variableId]
			if len(columnVariable.domain) == 0:
				return True

		return False

	# Different from Module2
	def initialFiltering(self):
		numberOfDeletedRowDomainVersions = 0
		numberOfDeletedColumnDomainVersions = 0
		for rowVariableId in self.rowVariables:
			for rowVariableVersion in self.rowVariables[rowVariableId].domain:

				for rowVariableDomainIndex in range(len(rowVariableVersion)):
					# For hver kolonne i raden

					isValid = False

					for columnVersion in self.columnVariables[rowVariableDomainIndex].domain:
						if columnVersion[self.rowVariables[rowVariableId].position] == rowVariableVersion[rowVariableDomainIndex]:
							isValid = True
							break

					if not isValid:
						self.rowVariables[rowVariableId].domain.remove(rowVariableVersion)
						if len(self.rowVariables[rowVariableId].domain) == 1:
							self.rowVariables[rowVariableId].setValue(self.rowVariables[rowVariableId].domain[0])
						numberOfDeletedRowDomainVersions += 1
						break

		for columnVariableId in self.columnVariables:
			for columnVariableVersion in self.columnVariables[columnVariableId].domain:

				for columnVariableDomainIndex in range(len(columnVariableVersion)):
					# For hver kolonne i raden

					isValid = False

					for rowVersion in self.rowVariables[columnVariableDomainIndex].domain:
						if rowVersion[self.columnVariables[columnVariableId].position] == columnVariableVersion[columnVariableDomainIndex]:
							isValid = True
							break

					if not isValid:
						self.columnVariables[columnVariableId].domain.remove(columnVariableVersion)
						if len(self.columnVariables[columnVariableId].domain) == 1:
							self.columnVariables[columnVariableId].setValue(self.columnVariables[columnVariableId].domain[0])
						numberOfDeletedColumnDomainVersions += 1
						break



		print "numberOfDeletedRowDomainVersions:", numberOfDeletedRowDomainVersions
		print "numberOfDeletedColumnDomainVersions:", numberOfDeletedColumnDomainVersions
