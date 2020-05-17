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
    mode = GameMode()
    mode.set_size(8)
    mode.set_arrangement([(Unit(KingMover()), 2, 2), (Unit(KingMover()), 1, 1)])
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
    mode = GameMode()
    mode.set_size(8)
    mode.set_arrangement([(Unit(RookMover()), 2, 2), (Unit(RookMover()), 2, 3)])
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


def test_bishop():
    mode = GameMode()
    mode.set_size(8)
    mode.set_arrangement([(Unit(BishopMover()), 2, 2), (Unit(BishopMover()), 3, 3)])
    board = Board(mode)
    x = 2
    y = 2
    assert board.do_move(2, 2, 4, 4) is False
    for i in range(8):
        for j in range(8):
            if i != x and j != y:
                board[i, j] = None

    for dx in range(-10, 10):
        for dy in range(-10, 10):
            if dx == 0 and dy == 0:
                continue
            to_x = x + dx
            to_y = y + dy
            if valid(to_x, to_y, 8):
                if abs(dx) == abs(dy):
                    assert board.do_move(x, y, to_x, to_y) is True
                    assert board.do_move(to_x, to_y, x, y) is True
                else:
                    assert board.do_move(x, y, to_x, to_y) is False


def test_police():
    mode = GameMode()
    mode.set_size(15)
    arrangement = [(Unit(PoliceManMover()), 4, 4)]
    x = 4
    y = 4
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0 or dx != dy:
                arrangement.append((Unit(KingMover()), x + dx, y + dy))
    mode.set_arrangement(arrangement)
    board = Board(mode)

    for i in range(15):
        for j in range(15):
            if board[i, j] is not None and board[i, j].player == board.player_B:
                board[i, j] = None

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            p_x = x + dx
            p_y = y + dy
            for d2x in range(-1, 2):
                for d2y in range(-1, 2):
                    if board[p_x + dx, p_y + dy] is None:
                        assert board.do_move(p_x, p_y, p_x + dx, p_y + dy) is True
                        assert board.do_move(p_x + dx, p_y + dy, p_x, p_y) is True

    for i in range(15):
        for j in range(15):
            if board[i, j] is not None and (i != 4 or j != 4):
                board[i, j].player = board.player_B

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            p_x = x + dx
            p_y = y + dy
            for d2x in range(-1, 2):
                for d2y in range(-1, 2):
                    assert board.do_move(p_x, p_y, p_x + dx, p_y + dy) is False

    x = 2
    y = 2
    mode.set_size(5)
    mode.set_arrangement([(Unit(PoliceManMover()), 2, 2)])
    board = Board(mode)
    for dx in range(-6, 6):
        for dy in range(-6, 6):
            if dx == dy and dx == 0:
                continue
            to_x = x + dx
            to_y = y + dy
            if valid(to_x, to_y, 6):
                if abs(dx) <= 1 and abs(dy) <= 1:
                    assert board.do_move(x, y, to_x, to_y) is True
                    assert board.do_move(to_x, to_y, x, y) is True
                else:
                    assert board.do_move(x, y, to_x, to_y) is False
