from board import Board
from gamemode import ClassicModeBuilder, Director, AllUnitsModeBuilder
from itertools import product
from gui.board_page import BoardPage
from gui.gui_operator import GuiOperator
import pygame


def test_classic():
    director = Director()
    mode = director.construct_game_mode(ClassicModeBuilder())
    board = Board(mode)
    assert board.is_game_finished() is None
    ex = (7, 0)
    for i, j in product(range(3), range(3)):
        board.do_move(i, j, ex[0], ex[1])
        ni, nj = 7 - i, 7 - j
        board.do_move(ni, nj, i, j)
        board.do_move(ex[0], ex[1], ni, nj)
    assert len(board.is_game_finished()) == 2
    board.do_move(7, 7, ex[0], ex[1])
    assert board.is_game_finished() is board.player_B
    board.do_move(ex[0], ex[1], 7, 7)
    board.do_move(0, 0, ex[0], ex[1])
    assert board.is_game_finished() is board.player_A
    assert board.is_game_finished() is board.player_A
    assert board.do_move(7, 7, 0, 0) is True
    assert board.is_game_finished() is None


def test_triangle():
    director = Director()
    mode = director.construct_game_mode(AllUnitsModeBuilder())
    board = Board(mode)
    for i in range(4):
        for j in range(3 - i):
            ni, nj = 8 - i, 8 - j
            assert board.map[i][j].type == board.map[ni][nj].type

    for i in range(4):
        for j in range(4 - i):
            ni, nj = 8 - i, 8 - j
            board.map[i][j], board.map[ni][nj] = board.map[ni][nj], board.map[i][j]

    board.map[0][0], board.map[4][4] = board.map[4][4], board.map[0][0]
    board.map[8][8], board.map[7][7] = board.map[7][7], board.map[8][8]

    assert board.is_game_finished() == board.player_A


def test_gui():
    pygame.init()
    screen = pygame.display.set_mode([800, 700])

    pygame.display.flip()
    director = Director()
    mode = director.construct_game_mode(ClassicModeBuilder())
    operator = GuiOperator()
    operator.state = BoardPage(screen, operator, mode)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            operator.state.handle(event)
            operator.state.draw()
            pygame.display.flip()

test_gui()
