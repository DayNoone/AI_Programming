import random, os
import pygame
import sys

background_color = (255, 255, 255)  # rbg
black = (0, 0, 0)
white = (255, 255, 255)
colors = [(255, 0, 0),  # RED
          (0, 255, 0),  # GREEN
          (0, 0, 255),  # BLUE
          (255, 255, 0),  # YELLOW
          (255, 0, 255),  # PURPLE
          (0, 255, 255),  # AQUA
          (255, 140, 0),  # ORANGE
          (255, 20, 147),  # PINK
          (128, 128, 128),  # GREY
          (165, 42, 42)]  # BROWN


def initiate(graph):
    global board_size, screen, multiplier, x_offset, y_offset, coffset
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (25, 50)  # forces screen to top left corner
    pygame.init()
    board_size = 700
    screen = pygame.display.set_mode((board_size, board_size + 0))
    pygame.display.set_caption('Module 2 - CSP-A*')

    # ---------- multiplyer to get complete graph within board
    x_size = graph[4][2] - graph[4][0]
    y_size = graph[4][3] - graph[4][1]
    if x_size > y_size:
        biggest = x_size
    else:
        biggest = y_size
    multiplier = (board_size - 20) / biggest

    # ---------- offset to correct certain graph coordinates of board
    x_offset, y_offset = 0 - graph[4][0], 0 - graph[4][1]
    coffset = 10  # Fixes so circles and variables stay within the board due to circle origo being coordinates


def draw_board(variables, graph, finished):
    pygame.time.wait(20)
    screen.fill(background_color)

    # ---------- draw connections
    for i in variables:
        for j in i.neighbor:
            if (j.colorid is not None or i.colorid is not None):  # only draw lines to variables with colors
                coordinates1 = ((i.xPos + x_offset) * multiplier + coffset, (i.yPos + y_offset) * multiplier + coffset)
                coordinates2 = ((j.xPos + x_offset) * multiplier + coffset, (j.yPos + y_offset) * multiplier + coffset)
                pygame.draw.line(screen, black, coordinates1, coordinates2, 2)


    # ---------- draw variables and fill with color
    for i in variables:
        coordinates = (int((i.xPos + x_offset) * multiplier) + coffset, int((i.yPos + y_offset) * multiplier) + coffset)
        if (i.colorid == None):
            pygame.draw.circle(screen, black, coordinates, 10, 3)

        else:
            pygame.draw.circle(screen, colors[i.colorid], coordinates, 10, 0)

    pygame.display.update()

    while finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
