from Project_1.genericAStarNode import AStarNode

class Node(AStarNode):
	def __init__(self, variables, initialDomain):
		self.variables = variables
		self.domainSize = initialDomain
		print initialDomain
