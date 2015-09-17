from Project_1.genericAStarNode import AStarNode

class Node(AStarNode):
	def __init__(self, variables, initialDomain, parent):
		self.variables = variables
		self.domainSize = initialDomain
		self.parent = parent
		self.gValue = 0
		self.hValue = 0
		self.fValue = self.gValue + self.hValue
		self.kids = []
		self.state = None
		self.state = self.calculateStateIndex()
		
	def checkIfGoalState(self):
		for variable in self.variables:
			if len(variable.domain) != 1:
				return False
		return True

	def checkIfContradiction(self):
		for variable in self.variables:
			if len(variable.domain) != 1:
				return False
		return True

	def calculateStateIndex(self):
		pass

	"""Algorithm methods"""

	@staticmethod
	def calculateHeuristicValue(self):
		pass

	@staticmethod
	def calculateGValue(self):
		pass

	@staticmethod
	def generate_all_successors(self):
		pass
