from gui import initiate, draw_board
from variable import Variable
import os

# boards = ['graph-color-1.txt', 'graph-color-2.txt', 'rand-50-4-color1.txt', 'rand-100-4-color1.txt',
# 		  'rand-100-6-color1.txt', 'spiral-500-4-color1.txt']

boards = ['gcolor1.txt', 'gcolor2.txt', 'gcolor3.txt']
K = [4, 4, 4, 4, 6, 4]


def readFile(path):
	with open(path) as f:
		nv_and_ne = [int(x) for x in f.readline().split()]  # read first line
		count = 0
		x_values = []
		y_values = []
		ixy = []
		for line in f:  # read rest of lines
			x = line.strip().split(' ')
			x[0] = int(x[0])
			x[1] = float(x[1])
			x[2] = float(x[2])
			x_values.append(x[1])
			y_values.append(x[2])
			ixy.append(x)
			count += 1
			if count == nv_and_ne[0]:
				break
		vertex = []
		for line in f:  # read rest of lines
			vertex.append([int(x) for x in line.split()])
	graph = nv_and_ne
	graph.append(ixy)
	graph.append(vertex)
	x_values.sort()
	y_values.sort()
	extremal_values = [x_values[0], y_values[0], x_values[-1], y_values[-1]]
	graph.append(extremal_values)
	return graph


def create_Variables(graph, k):
	variables = {}
	constraints = {}
	for i in graph[2]:  # creates variables using id and pos
		variableID = i[0]
		v = Variable(variableID, i[1], i[2], [x for x in range(k)])
		variables[v.id] = v
		constraints[variableID] = []
	for i in graph[3]:  # adds lines between variables
		VariableID1 = i[0]
		VariableID2 = i[1]
		constraints[VariableID1].append(VariableID2)
		constraints[VariableID2].append(VariableID1)
	for variableId in variables:
		variable = variables[variableId]
		variable.constraints = constraints
	return variables


def readBoard(no):
	if os.name == 'nt':
		return readFile('graphs\\' + no)
	else:
		return readFile('graphs/' + no)


def inputValidation(inputText):
	while True:
		try:
			return int(raw_input(inputText))
		except ValueError:
			print('Please enter an integer...')
