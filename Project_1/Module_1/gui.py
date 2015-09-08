import pygame, sys
from pygame.locals import *

#contants representing colours
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#constants representing the different resources
START = 'S'
GOAL = 'X'
BARRIER = '#'
EMPTY_SPACE = 'O'

#a dictionary linking resources to colours
colors = {
    'S'    : RED,
    'X'    : GREEN,
    '#'    : GREY,
    'O'    : WHITE,
    'P'    : BLUE
}

#a list representing our tilemap
tilemap = [
    ['S', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', '#', '#', '#'],
    ['O', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O']
]
tilemap2 = [
    ['S', 'P', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', '#', '#', '#'],
    ['O', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O']
]
tilemap3 = [
    ['S', 'P', 'P', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', '#', '#', '#'],
    ['O', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O']
]



#useful game dimesions
TILESIZE = 50
MAPWIDTH = 4
MAPHEIGH = 5

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGH*TILESIZE))

def drawBoard(map, finished):
    #loop through each row
    for row in range(MAPHEIGH):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilmap, using the cc
            pygame.draw.rect(DISPLAYSURF, colors[map[row][column]], (column*TILESIZE, row*TILESIZE,TILESIZE,TILESIZE))
            pygame.draw.circle(DISPLAYSURF, BLACK, ((column*TILESIZE)+TILESIZE/2, (row*TILESIZE)+TILESIZE/2), 3, 0)

    #update the display
    pygame.display.flip()
    pygame.time.wait(400)
    while finished:
    #get all the user events
        for event in pygame.event.get():
            #if the user wants to quit
            if event.type == QUIT:
                #and the game and close the window
                pygame.quit()
                sys.exit()


drawBoard(tilemap, False)
drawBoard(tilemap2, False)
drawBoard(tilemap3, True)