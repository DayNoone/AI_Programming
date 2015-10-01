import copy
from gui import initiate, draw_board
from variable import Variable
from Project_1.genericAStarNode import AStarNode


class Node(AStarNode):
	def __init__(self, variables, parent):
		self.variables = variables
		self.parent = parent
		self.gValue = self.calculateGValue()
		self.hValue = self.calculateHeuristicValue()
		self.fValue = self.gValue + self.hValue
		self.kids = []
		self.state = self.calculateStateIndex()
		AStarNode.__init__(self, parent)

	def checkIfGoalState(self):
		for variableId in self.variables:
			if len(self.variables[variableId].domain) != 1:
				return False
		return True

	def checkIfContradiction(self):
		for variableId in self.variables:
			if len(self.variables[variableId].domain) == 0:
				return True
		return False

	def calculateStateIndex(self):
		string = "0"
		for variableId in self.variables:
			if self.variables[variableId].colorid is not None:
				string += str(variableId) + str(self.variables[variableId].colorid) + "999"
		return int(string)

	"""Algorithm methods"""

	def calculateHeuristicValue(self):
		numberOfTotalDomain = 0
		for variableId in self.variables:
			numberOfTotalDomain += len(self.variables[variableId].domain)

		if self.checkIfContradiction():
			heuristic = 999999
		else:
			heuristic = numberOfTotalDomain

		return heuristic

	def calculateHeuristicValue2(self):
		numberOfColoredVariables = 0
		for variableId in self.variables:
			if self.variables[variableId].colorid is not None:
				numberOfColoredVariables += 1

		if self.checkIfContradiction():
			heuristic = 999999
		else:
			heuristic = len(self.variables) - numberOfColoredVariables

		return heuristic

	def calculateGValue(self):
		if self.parent is None:
			return 0
		return self.parent.gValue + self.MOVEMENT_COST

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

	def revise(self, variable):
		reviseQueue = [variable]

		while len(reviseQueue) != 0:
			newVariable = reviseQueue.pop(0)

			for neighbor in newVariable.neighbors:
				if newVariable.colorid in neighbor.domain:
					neighbor.domain.remove(newVariable.colorid)
				if len(neighbor.domain) == 1 and neighbor.colorid is None:
					neighbor.colorid = neighbor.domain[0]
					reviseQueue.append(neighbor)

	def drawBoard(self, openNodes, closedNodes, isFinished):
		draw_board(self.variables, isFinished)
