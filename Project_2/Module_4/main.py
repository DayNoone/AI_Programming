from Tkinter import Tk
from board import Board, initBoard
from visuals import GameWindow

testBoardList = [0, 2, 4, 4,
                 0, 2, 1, 3,
                 0, 1, 1, 3,
                 0, 0, 2, 1]

test_board_list_1 = [1, 2, 3, 4,
                     5, 6, 7, 8,
                     9, 10, 11, 12,
                     13, 14, 16, 16]

testBoard = Board(testBoardList)
testBoard1 = Board(test_board_list_1)

gameBoard = initBoard()


def leftKey(event):
	gameBoard.moveLeft()
	gameBoard.placeRandomTwoOrFour()

	window.update_view(gameBoard.board)


def rightKey(event):
	gameBoard.moveRight()
	gameBoard.placeRandomTwoOrFour()

	window.update_view(gameBoard.board)


def upKey(event):
	gameBoard.moveUp()
	gameBoard.placeRandomTwoOrFour()

	window.update_view(gameBoard.board)


def downKey(event):
	gameBoard.moveDown()
	gameBoard.placeRandomTwoOrFour()
	window.update_view(gameBoard.board)


def keyReleased(event):
	if event.char == 'r':
		gameBoard.restartGame()
		window.update_view(gameBoard.board)


main = Tk()

window = GameWindow(main)

window.update_view(gameBoard.board)  # 1D list representing the board

main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
main.bind('<Up>', upKey)
main.bind('<Down>', downKey)
main.bind('<KeyRelease>', keyReleased)

window.pack()

window.mainloop()
