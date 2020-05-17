from unit import Type, Unit, FlexMover, KingMover
from enum import Enum
from board import Board, valid
from gamemode import ClassicModeBuilder, Director, GameMode
from unit import *

class CustomType(Enum):
    SUPER = 0


def test_changing_type():
    figure = Unit(FlexMover())
    assert figure.type == Type.FLEX
    figure.set_mover(KingMover())
    assert figure.type == Type.KING
    figure.type = CustomType.SUPER
    assert figure.type == CustomType.SUPER
    figure.set_mover(FlexMover(), keep_type=True)
    assert figure.type == CustomType.SUPER
    assert figure.type != Type.PAWN


def test_pawn():
    director = Director()
    mode = director.construct_game_mode(ClassicModeBuilder())
    board = Board(mode)

    for i in range(2, -1, -1):
        for j in range(3):
            board.do_move(i, j, i + 5, j)
            board.do_move(7 - i, 7 - j, 2 - i, 7 - j)

    for i in range(3):
        for j in range(3):
            assert board[i + 5, j] is not None
            assert board[i, j + 5] is not None
            assert board[i, j] is None
            assert board[i + 5, j + 5] is None

    board = Board(mode)
    for i in range(1, 8):
        for j in range(8):
            board[i, j] = None

    for i in range(1, 8):
        for j in range(8):
            if i != 0 and j != 2:
                assert board.do_move(0, 2, i, j) is False


def test_king():
    mode = GameMode(8, [(Unit(KingMover()), 2, 2), (Unit(KingMover()), 1, 1)])
    board = Board(mode)
    x = 2
    y = 2

    assert board.do_move(2, 2, 1, 1) is False
    board[1, 1] = None

    for dx in range(-10, 10):
        for dy in range(-10, 10):
            if dx == dy == 0:
                continue
            to_x = x + dx
            to_y = y + dy
            if valid(to_x, to_y, 8):
                if abs(dx) <= 1 and abs(dy) <= 1:
                    assert board.do_move(x, y, to_x, to_y) is True
                    assert board.do_move(to_x, to_y, x, y) is True
                else:
                    assert board.do_move(x, y, to_x, to_y) is False


def test_rook():
    mode = GameMode(8, [(Unit(RookMover), 2, 2), (Unit(RookMover()), 2, 3)])
    board = Board(mode)
    x = 2
    y = 2
    assert board.do_move(2, 2, 2, 6) is False
    board[2, 3] = None

    for dx in range(-10, 10):
        for dy in range(-10, 10):
            if dx == dy == 0:
                continue
            to_x = x + dx
            to_y = y + dy
            if valid(to_x, to_y, 8):
                if dx == 0 or dy == 0:
                    assert board.do_move(x, y, to_x, to_y) is True
                    assert board.do_move(to_x, to_y, x, y) is True
                else:
                    assert board.do_move(x, y, to_x, to_y) is False



