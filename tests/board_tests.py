from board import Board
from gamemode import ClassicModeBuilder, Director
from itertools import product


def test_classic():
    director = Director()
    mode = director.construct_game_mode(ClassicModeBuilder())
    board = Board(mode)
    assert board.is_game_finished() is None
    ex = (7, 0)
    for i, j in product(range(8), range(8)):
        board.do_move(i, j, ex[0], ex[1])
        ni, nj = 7 - i, 7 - j
        board.do_move(ni, nj, i, j)
        board.do_move(ex[0], ex[1], ni, nj)
    assert len(board.is_game_finished()) == 2
    board.do_move(7, 7, ex[0], ex[1])
    assert board.is_game_finished() is board.player_A
    board.do_move(ex[0], ex[1], 7, 7)
    board.do_move(0, 0, ex[0], ex[1])
    assert board.is_game_finished() is board.player_B
