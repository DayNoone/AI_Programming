from variable import Variable
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
		self.state = self.calculateStateIndex()

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

	@staticmethod
	def calculateHeuristicValue(self):
		# TODO
		return 1

	@staticmethod
	def calculateGValue(self):
		if self.parent is None:
			return 0
		return self.parent.gValue + self.MOVEMENT_COST

	@staticmethod
	def generate_all_successors(self):
		# TODO
		#	   Generating their successor states (by makin assumptions)
		#	   Enforcing the assumption in each successor state by reducing the domain of the assumed variable to a singleton set
		#	   Calling GAC-Rerun on each newly-generated state
		#	   Computing the f, g and h values for each new state,
		#		   where h i based on the state of the CSP after the call to GAC-Rerun
		pass
