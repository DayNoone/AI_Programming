from Board import Board

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

    # for a in board:
    #     for b in a:
    #         print b,
    #     print ''

    return board


def getBoardInfoFromInput():
    dimX = raw_input("DimensionX: ")
    dimY = raw_input("DimensionY: ")
    startX = raw_input("StartX: ")
    startY = raw_input("StartY: ")
    goalX = raw_input("GoalX: ")
    goalY = raw_input("GoalY: ")
    barriers = []
    while 1:
        prompt = raw_input("Do you want to enter one more barrier? y/n")
        if prompt == 'y':
            barrierXpos = int(raw_input("Enter barrier Xpos: "))
            barrierYpos = int(raw_input("Enter barrier Ypos: "))
            barrierXRange = int(raw_input("Enter barrier XRange: "))
            barrierYRange = int(raw_input("Enter barrier YRange: "))
            barriers.append([barrierXpos, barrierYpos, barrierXRange, barrierYRange])
        elif prompt == 'n':
            break
    return Board(generateBoard(int(dimX), int(dimY), int(startX), int(startY), int(goalX), int(goalY), barriers), (int(startX), int(startY)), (int(goalX), int(goalY)))


board_test = Board(generateBoard(6, 6, 1, 0, 5, 5, [[3, 2, 2, 2], [0, 3, 1, 3], [2, 0, 4, 2], [2, 5, 2, 1]]), (1, 0), (5, 5))
board_0 = Board(generateBoard(10, 10, 0, 0, 9, 9, [[2, 3, 5, 5], [8, 8, 2, 1]]), (0, 0), (9, 9))
board_1 = Board(generateBoard(20, 20, 19, 3, 2, 18, [[5, 5, 10, 10], [1, 2, 4, 1]]), (19, 3), (2, 18))
board_2 = Board(generateBoard(20, 20, 0, 0, 19, 19, [[17, 10, 2, 1], [14, 4, 5, 2], [3, 16, 10, 2], [13, 7, 5, 3], [15, 15, 3, 3]]),(0, 0), (19, 19))
board_3 = Board(generateBoard(10, 10, 0, 0, 9, 5, [[3, 0, 2, 7], [6, 0, 4, 4], [6, 6, 2, 4]]), (0, 0), (9, 5))
board_4 = Board(generateBoard(10, 10, 0, 0, 9, 9, [[3, 0, 2, 7], [6, 0, 4, 4], [6, 6, 2, 4]]), (0, 0), (9, 9))
board_5 = Board(generateBoard(20, 20, 0, 0, 19, 13, [[4, 0, 4, 16], [12, 4, 2, 16], [16, 8, 4, 4]]),(0, 0), (19, 13))
board_angle = Board(generateBoard(20, 20, 0, 0, 19, 19, [[1, 18, 18, 1], [18, 1, 1, 18]]), (0, 0), (19, 19))


def getBoardExampleList():
    return [board_0, board_1, board_2, board_3, board_4, board_5, board_test, board_angle]
