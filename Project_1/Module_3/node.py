import copy
from Project_1.genericCSPNode import CSPNode
from gui import initiate, draw_board


class Node(CSPNode):
	def __init__(self, rowVariables, columnVariables, parent, x_dimension, y_dimension):
		self.rowVariables = rowVariables
		self.columnVariables = columnVariables
		self.variables = {}
		self.variables.update(self.rowVariables)
		self.variables.update(self.columnVariables)
		self.parent = parent
		self.x_dimension = x_dimension
		self.y_dimension = y_dimension
		self.state = self.calculateStateIndex()
		CSPNode.__init__(self, parent)

	def generate_all_successors(self):
		# TODO: Do better! Start with domainSize of first variable?
		smallestVariable, smallestVariableDomainSize = self.findSmallestVariable(self.variables)

		successors = []

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

			variable.value = value
			variable.domain = [value]
			newNode = Node(rowVariablesCopy, columnVariablesCopy, self, self.x_dimension, self.y_dimension)
			# newNode.revise(variable)
			newNode.revise()

			successors.append(newNode)

		return successors

	def calculateStateIndex(self):
		string = "0"
		for rowVariableId in self.rowVariables:
			rowVariable = self.rowVariables[rowVariableId]
			if rowVariable.value is not None:
				string += str(rowVariableId) + ''.join(str(i) for i in rowVariable.value) + "999"

		for columnVariableId in self.columnVariables:
			columnVariable = self.columnVariables[columnVariableId]
			if columnVariable.value is not None:
				string += str(columnVariableId) + ''.join(str(i) for i in columnVariable.value) + "999"

		return int(string)

	# Different from Module2
	def revise(self):
		numberOfDeletedRowDomainVersions = 0
		numberOfDeletedColumnDomainVersions = 0
		for rowVariableId in self.rowVariables:
			rowVariable = self.rowVariables[rowVariableId]
			for rowVariableVersion in rowVariable.domain:

				for rowVariableDomainIndex in range(len(rowVariableVersion)):
					# For hver kolonne i raden

					isValid = False

					for columnVersion in self.columnVariables[self.getVariableKey(1, rowVariableDomainIndex)].domain:
						if columnVersion[rowVariable.position] == rowVariableVersion[rowVariableDomainIndex]:
							isValid = True
							break

					if not isValid:
						rowVariable.domain.remove(rowVariableVersion)
						if len(rowVariable.domain) == 1:
							rowVariable.value = rowVariable.domain[0]
						numberOfDeletedRowDomainVersions += 1
						break

		for columnVariableId in self.columnVariables:
			columnVariable = self.columnVariables[columnVariableId]
			for columnVariableVersion in columnVariable.domain:

				for columnVariableDomainIndex in range(len(columnVariableVersion)):
					# For hver kolonne i raden

					isValid = False

					for rowVersion in self.rowVariables[self.getVariableKey(0, columnVariableDomainIndex)].domain:
						if rowVersion[columnVariable.position] == columnVariableVersion[columnVariableDomainIndex]:
							isValid = True
							break

					if not isValid:
						columnVariable.domain.remove(columnVariableVersion)
						if len(columnVariable.domain) == 1:
							columnVariable.value = columnVariable.domain[0]
						numberOfDeletedColumnDomainVersions += 1
						break



					# print "numberOfDeletedRowDomainVersions:", numberOfDeletedRowDomainVersions
					# print "numberOfDeletedColumnDomainVersions:", numberOfDeletedColumnDomainVersions

	@staticmethod
	def getVariableKey(rowOrColumn, position):
		return int(str(9) + str(rowOrColumn) + str(11111) + str(position))

	"""ONLY FOR GUI"""

	def generateBoard(self):
		board = [[0 for column in range(self.x_dimension)] for row in range(self.y_dimension)]
		for variableId in self.rowVariables:
			variable = self.rowVariables[variableId]
			if len(variable.domain) == 1:
				if variable.type == 0:
					if variable.value == None:
						print "none"
					for column in range(len(variable.value)):
						board[variable.position][column] = variable.value[column]
				else:
					for row in range(len(variable.value)):
						board[row][variable.position] = variable.value[row]

		for variableId in self.columnVariables:
			variable = self.columnVariables[variableId]
			if len(variable.domain) == 1:
				if variable.type == 0:
					for column in range(len(variable.value)):
						board[variable.position][column] = variable.value[column]
				else:
					for row in range(len(variable.value)):
						board[row][variable.position] = variable.value[row]

		return board

	# Different from Module2
	def drawBoard(self, openNodes, closedNodes, isFinished):
		board = self.generateBoard()
		draw_board(board, isFinished)
