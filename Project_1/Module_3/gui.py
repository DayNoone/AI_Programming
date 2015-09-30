import random, os
import pygame
import sys

def initiate(board):
    global TILESIZE, DISPLAYSURF
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 50)  # forces screen to top left corner
    pygame.init()
    pygame.display.set_caption('Module 3 - Nonograms')
    TILESIZE = 50
    DISPLAYSURF = pygame.display.set_mode((len(board[0]) * TILESIZE, len(board) * TILESIZE))




def draw_board(board, finished):
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 0:
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (column * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, (30, 144, 255), (column * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE))

    pygame.display.update()

    while finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

