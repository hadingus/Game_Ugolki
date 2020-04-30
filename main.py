from copy import deepcopy
from unit import *
from gamemode import *
from gui.components import Button
from gui.start_page import StartPage
from gui.mode_page import ModePage
from gui.gui_operator import GuiOperator
import pygame

from board import Board


def main():
    pygame.init()
    screen = pygame.display.set_mode([512, 512])

    pygame.display.flip()

    operator = GuiOperator()
    startPage = StartPage(screen, operator)
    operator.state = startPage
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            operator.state.handle(event)
            operator.state.draw()
            pygame.display.flip()

    board = Board(dir.construct_game_mode(b[0]))
    board.print_board()

    print("First board is correct")

    board.reformat(dir.construct_game_mode(b[3]))
    board.print_board()

    print("Second board is correct")


if __name__ == '__main__':
    main()

