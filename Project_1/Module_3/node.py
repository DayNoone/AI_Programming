import copy
from Project_1.genericCSPNode import CSPNode
from gui import initiate, draw_board


class Node(CSPNode):
    def __init__(self, rowVariables, columnVariables, parent, x_dimension, y_dimension):
        self.rowVariables = rowVariables
        self.columnVariables = columnVariables
        self.parent = parent
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.state = self.calculateStateIndex()
        CSPNode.__init__(self, parent)

    def calculateHeuristicValue(self):
        # TODO: Calculate heuristic
        numberOfTotalDomain = self.addDomains(self.rowVariables) + self.addDomains(self.columnVariables)

        if self.checkIfContradiction():
            heuristic = 999999
        else:
            heuristic = numberOfTotalDomain

        return heuristic

    def generate_all_successors(self):
        smallestVariable = None
        # TODO: Do better! Start with domainSize of first variable?
        smallestVariableDomainSize = 999
        smallestVariable, smallestVariableDomainSize = self.findSmallestVariable(self.rowVariables, smallestVariable, smallestVariableDomainSize)
        smallestVariable, smallestVariableDomainSize = self.findSmallestVariable(self.columnVariables, smallestVariable, smallestVariableDomainSize)


        # TODO: Stop if domainsize == 2?? Maybe not faster

        successors = []

        if smallestVariable == None:
            print "asdf"

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
            newNode.initialFiltering()

            successors.append(newNode)

        return successors

    # Different from Module2
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
    def drawBoard(self, openNodes, closedNodes, isFinished):
        board = self.generateBoard()
        draw_board(board, isFinished)

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

    def checkIfGoalState(self):

        for variableId in self.rowVariables:
            variable = self.rowVariables[variableId]
            if len(variable.domain) != 1:
                return False

        for variableId in self.columnVariables:
            variable = self.columnVariables[variableId]
            if len(variable.domain) != 1:
                return False

        return True

    def checkIfContradiction(self):
        for variableId in self.rowVariables:
            rowVariable = self.rowVariables[variableId]
            if len(rowVariable.domain) == 0:
                return True

        for variableId in self.columnVariables:
            columnVariable = self.columnVariables[variableId]
            if len(columnVariable.domain) == 0:
                return True

        return False

    # Different from Module2
    def initialFiltering(self):
        numberOfDeletedRowDomainVersions = 0
        numberOfDeletedColumnDomainVersions = 0
        for rowVariableId in self.rowVariables:
            rowVariable = self.rowVariables[rowVariableId]
            for rowVariableVersion in rowVariable.domain:

                for rowVariableDomainIndex in range(len(rowVariableVersion)):
                    # For hver kolonne i raden

                    isValid = False

                    for columnVersion in self.columnVariables[rowVariableDomainIndex].domain:
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

                    for rowVersion in self.rowVariables[columnVariableDomainIndex].domain:
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
