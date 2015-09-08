def generateBoard(dimensionX, dimensionY, startX, startY, goalX, goalY, barriers):
    board = [['O' for x in range(dimensionX)] for x in range(dimensionY)]

    board[startX][startY] = 'S'
    board[goalX][goalY] = 'X'

    for barrier in barriers:
        xStart = barrier[0]
        yStart = barrier[1]
        xRange = barrier[2]
        yRange = barrier[3]

        for xPos in range(xStart, xStart + xRange):
            for yPos in range(yStart, yStart + yRange):
                board[xPos][yPos] = '#'

    for a in board:
        for b in a:
            print b,
        print ''

    return board


def getBoardInfoFromInput():
    dimX = raw_input("DimensionX: ")
    dimY = raw_input("DimensionY: ")
    startX = raw_input("StartX: ")
    startY = raw_input("StartY: ")
    goalX = raw_input("GoalX: ")
    goalY = raw_input("GoalY: ")
    barriers = []
    print "Enter barriers: startX startY rangeX rangeY. I.e 0022"
    print "Generate board with: q"
    while 1:
        prompt = raw_input("Do you want to enter one more barrier? y/n")
        if prompt == 'y':
            barrierXpos = int(raw_input("Enter barrier Xpos: "))
            barrierYpos = int(raw_input("Enter barrier Ypos: "))
            barrierXRange = int(raw_input("Enter barrier XRange: "))
            barrierYRange = int(raw_input("Enter barrier YRange: "))
            barriers.append([barrierXpos, barrierYpos, barrierXRange, barrierYRange])
        elif prompt == 'n':
            break;
    generateBoard(int(dimX), int(dimY), int(startX), int(startY), int(goalX), int(goalY), barriers)

# generateBoard(6, 6, 1, 0, 5, 5, [[3, 2, 2, 2], [0, 3, 1, 3], [2, 0, 4, 2], [2, 5, 2, 1]])
getBoardInfoFromInput()
