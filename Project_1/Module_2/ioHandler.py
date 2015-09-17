from gui import initiate, draw_board
from Variable2 import Variable
import os

boards = ['graph-color-1.txt', 'graph-color-2.txt', 'rand-50-4-color1.txt', 'rand-100-4-color1.txt', 'rand-100-6-color1.txt', 'spiral-500-4-color1.txt']
K = [4, 4, 4, 4, 6, 4]

def readFile(path):
    with open(path) as f:
        nv_and_ne = [int(x) for x in f.readline().split()] # read first line
        count = 0
        x_values = []
        y_values = []
        ixy = []
        for line in f: # read rest of lines
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
        for line in f: # read rest of lines
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
    Variables = []
    for i in graph[2]: # creates Variables using id and pos
        Variables.append(Variable(i[0], i[1], i[2], k))
    for i in graph[3]: # adds lines between Variables
        Variable1 = i[0]
        Variable2 = i[1]
        Variables[Variable1].neighbor.append(Variable2) # adds another neighbor
        Variables[Variable2].neighbor.append(Variable1) # has to add to other neighbor aswell
        #print Variables[Variable1].neighbor, Variables[Variable2].neighbor
    return Variables

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