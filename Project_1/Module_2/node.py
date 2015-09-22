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
		for variable in self.variables:
			if len(variable.domain) != 1:
				return False
		return True

	def checkIfContradiction(self):
		for variable in self.variables:
			if len(variable.domain) == 0:
				return True
		return False

	def calculateStateIndex(self):
		string = "0"
		for variable in self.variables:
			if variable.colorid is not None:
				string += str(variable.id) + str(variable.colorid) + "999"
		return string

	"""Algorithm methods"""

	def calculateHeuristicValue(self):
		numberOfColoredVariables = 0
		for variable in self.variables:
			if variable.colorid is not None:
				numberOfColoredVariables += 1

		if self.checkIfContradiction():
			heuristic = 999999
		else:
			heuristic = len(self.variables)-numberOfColoredVariables

		return heuristic

	def calculateGValue(self):
		if self.parent is None:
			return 0
		return self.parent.gValue + self.MOVEMENT_COST

	def generate_all_successors(self):
		smallestVariable = None
		smallestVariableDomainSize = 999
		for variable in self.variables:
			if 1 < len(variable.domain) < smallestVariableDomainSize:
				smallestVariable = variable
				smallestVariableDomainSize = len(smallestVariable.domain)

		successors = []


		for value in smallestVariable.domain:
			variablesCopy = copy.deepcopy(self.variables)
			for variable in variablesCopy:
				if variable.id == smallestVariable.id:
					variable.colorid = value
					variable.domain = [value]
					newNode = Node(variablesCopy, self)
					newNode.revise(variable)

					successors.append(newNode)
					break;

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
		draw_board(self.variables, False)
