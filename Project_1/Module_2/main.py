from ioHandler import *
import os


def main():
    board = inputValidation('Choose board (0-5): ')

    if os.name == 'nt':
        graph = readFile('graphs\\' + boards[board])
    else:
        graph = readFile('graphs/' + boards[board])

    initiate(graph)
    variables = create_Variables(graph)
    variables[0].colorid = 2
    variables[2].colorid = 2
    variables[3].colorid = 2
    draw_board(variables, graph, True)


main()
