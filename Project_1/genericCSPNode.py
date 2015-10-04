from Project_1.genericAStarNode import AStarNode


def countDomainValues(variables):
	numberOfTotalDomain = 0
	for variableId in variables:
		numberOfTotalDomain += len(variables[variableId].domain)
	return numberOfTotalDomain


class CSPNode(AStarNode):
	def __init__(self, parent):
		AStarNode.__init__(self, parent)

	def calculateStateIndex(self):
		raise NotImplementedError

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

	def calculateHeuristicValue(self):

		if self.checkIfContradiction():
			heuristic = 999999
		else:
			numberOfTotalDomain = countDomainValues(self.variables)
			heuristic = numberOfTotalDomain

		return heuristic

	def drawBoard(self, openNodes, closedNodes, isFinished):
		raise NotImplementedError

	def generate_all_successors(self):
		raise NotImplementedError

	@staticmethod
	def findSmallestVariable(variables):
		smallestVariable = None,
		smallestVariableDomainSize = 9999
		for k,rowVariable in variables.iteritems():
			# rowVariable = variables[variableId]
			if 1 < len(rowVariable.domain) < smallestVariableDomainSize:
				smallestVariable = rowVariable
				smallestVariableDomainSize = len(smallestVariable.domain)
		return smallestVariable, smallestVariableDomainSize
