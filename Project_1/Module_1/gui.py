import pygame, sys
from pygame.locals import *

#contants representing colours
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
BLACK = (0, 0, 0)
RED = (178, 34, 34)
GREEN = (173, 255, 47)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)

#constants representing the different resources
START = 'S'
GOAL = 'X'
BARRIER = '#'
EMPTY_SPACE = 'O'

#a dictionary linking resources to colours
colors = {
    'S'    : RED,
    'X'    : RED,
    '#'    : GREY,
    'O'    : WHITE,
    '1'    : BLUE
}

#useful game dimesions
TILESIZE = 25
MAPWIDTH = 0
MAPHEIGH = 0

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((20*TILESIZE, 20*TILESIZE))

def initiate(board):
    global MAPHEIGH
    MAPHEIGH = len(board)
    global MAPWIDTH
    MAPWIDTH = len(board[0])


def addNodePos(node, pathMat):
    pathMat[node.xPos][node.yPos] = '1'
    if node.parent is not None:
        addNodePos(node.parent, pathMat)


def generatePathMatrix(node):

    pathMat = [[0 for x in range(MAPWIDTH)] for x in range(MAPHEIGH)]
    addNodePos(node, pathMat)
    return pathMat


def drawSolution(node):
    if node.parent is not None:
        pygame.draw.line(DISPLAYSURF, BLACK, ((node.yPos*TILESIZE)+TILESIZE/2, (node.xPos*TILESIZE)+TILESIZE/2), ((node.parent.yPos*TILESIZE)+TILESIZE/2, (node.parent.xPos*TILESIZE)+TILESIZE/2), 1)
        drawSolution(node.parent)


def drawBoard(node, board, openNodes, closedNodes, finished):
    # pygame.time.wait(100)
    pathMat = generatePathMatrix(node)
    #loop through each row
    for row in range(MAPHEIGH):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilmap, using the cc
            pygame.draw.rect(DISPLAYSURF, colors[board[row][column]], (column*TILESIZE, row*TILESIZE,TILESIZE,TILESIZE))
            pygame.draw.circle(DISPLAYSURF, BLACK, ((column*TILESIZE)+TILESIZE/2, (row*TILESIZE)+TILESIZE/2), 3, 0)
            if pathMat[row][column] == '1':
                #draw the resource at that position in the tilmap, using the cc
                pygame.draw.rect(DISPLAYSURF, colors[pathMat[row][column]], (column*TILESIZE, row*TILESIZE,TILESIZE,TILESIZE))
                pygame.draw.circle(DISPLAYSURF, BLACK, ((column*TILESIZE)+TILESIZE/2, (row*TILESIZE)+TILESIZE/2), 3, 0)

    for node in openNodes:
        pygame.draw.rect(DISPLAYSURF, GREEN, (node.yPos*TILESIZE, node.xPos*TILESIZE,TILESIZE,TILESIZE))
        pygame.draw.circle(DISPLAYSURF, BLACK, ((node.yPos*TILESIZE)+TILESIZE/2, (node.xPos*TILESIZE)+TILESIZE/2), 3, 0)

    for node in closedNodes:
        pygame.draw.rect(DISPLAYSURF, YELLOW, (node.yPos*TILESIZE, node.xPos*TILESIZE,TILESIZE,TILESIZE))
        pygame.draw.circle(DISPLAYSURF, BLACK, ((node.yPos*TILESIZE)+TILESIZE/2, (node.xPos*TILESIZE)+TILESIZE/2), 3, 0)



    if finished:
        drawSolution(node)


    #update the display
    pygame.display.flip()
    # pygame.time.wait(10)
    while finished:
    #get all the user events
        for event in pygame.event.get():
            #if the user wants to quit
            if event.type == QUIT:
                #and the game and close the window
                pygame.quit()
                sys.exit()