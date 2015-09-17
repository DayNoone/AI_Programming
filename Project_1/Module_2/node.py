from Project_1.genericAStarNode import AStarNode

class node(AStarNode):
	def __init__(self, variables, initialDomain):
		self.variables = variables
		self.domainSize = initialDomain
		print initialDomain