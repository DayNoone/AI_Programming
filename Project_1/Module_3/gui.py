import random, os
import pygame
import sys

def initiate():
    global x_size, y_size
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 50)  # forces screen to top left corner
    pygame.init()
    board_size = 750
    screen = pygame.display.set_mode((board_size, board_size + 0))
    pygame.display.set_caption('Module 3 - Nonograms')

    board = [[0 for y in range(y_size)] for x in range(x_size)]



def draw_board(board, finished):

    pygame.display.update()

    while finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

