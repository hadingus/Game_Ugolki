import copy
from enum import Enum
from abc import ABC, abstractmethod
from player import Player
from itertools import product


class Unit:
    __next_id = 0

    def __init__(self, mover: 'Mover'):
        self.player = None
        self.id = Unit.__next_id
        self._mover = mover
        self._type = mover.type
        self._board = None

    def __copy__(self):
        new_unit = self.__class__(self._mover)
        new_unit.player = self.player
        new_unit._mover = self._mover
        new_unit._type = self._type
        new_unit._board = self._board
        return new_unit

    def __deepcopy__(self, memo={}):
        new_unit = self.__class__(self._mover)
        new_unit._mover = copy.deepcopy(self._mover, memo)
        new_unit.player = copy.deepcopy(self.player)
        new_unit._type = self._type
        new_unit._board = self._board
        return new_unit

    def set_player(self, player: Player):
        self.player = player

    def __hash__(self):
        return hash(id)

    def can_move(self, position):
        if self._board is None:
            raise ValueError('Board is not set')
        return self._mover.can_move(self, self._board, position)

    def set_board(self, board):
        self._board = board

    def set_mover(self, new_mover, *, keep_type=False):
        # In some ways unit.type may alter from unit._mover.type
        self._mover = new_mover
        if not keep_type:
            self._type = self._mover.type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type


class Mover(ABC):
    type = None

    def can_move(self, unit: Unit, board, position):
        start_position = board.position_of_unit[unit]
        positions = self._possible_positions(unit, board)
        if position in positions:
            return True
        return False

    def _possible_positions(self, unit: Unit, board):
        if not self._can_move(unit, board):
            return {}
        return self._positions_without_block(unit, board)

    def _can_move(self, unit: Unit, board):
        police_block = 3

        x, y = board.position_of_unit[unit]

        for nx, ny in product(range(x - police_block // 2, x + police_block // 2 + 1),
                              range(y - police_block // 2, y + police_block // 2 + 1)):
            if (x, y) == (nx, ny):
                continue
            if 0 <= nx < board.size_map and 0 <= ny < board.size_map:
                if board[nx, ny] is not None and \
                        board[nx, ny].type == Type.POLICE and board[nx, ny].player is not unit.player:
                    return False

        return True

    @abstractmethod
    def _positions_without_block(self, unit: Unit, board):
        ...


class Type(Enum):
    PAWN = 0
    KING = 1
    USUAL = 2
    FLEX = 3
    SNAKE = 4
    BISHOP = 5
    ROOK = 6
    SWAP = 7
    POLICE = 8
    CHECKERS_KING = 9


class PawnMover(Mover):
    type = Type.PAWN

    def _positions_without_block(self, unit: Unit, board):
        position = board.position_of_unit[unit]
        return {
            (position[0], position[1] + 1),
            (position[0], position[1] - 1),
            (position[0] + 1, position[1]),
            (position[0] - 1, position[1])
        }


class KingMover(Mover):
    type = Type.KING

    def _positions_without_block(self, unit: Unit, board):
        x, y = board.position_of_unit[unit]

        result = set()
        for nx, ny in product(range(x - 1, x + 2), range(y - 1, y + 2)):
            if (nx, ny) != (x, y):
                result.add((nx, ny))
        return result


class UsualMover(Mover):
    type = Type.USUAL

    # def move(self, unit, board, position):
    #     print("Usual figure moves")

    def _positions_without_block(self, unit: Unit, board):
        return RookMover()._positions_without_block(unit, board)


class FlexMover(Mover):
    type = Type.FLEX

    def _positions_without_block(self, unit: Unit, board):
        print("Flex figure moves")


class SnakeMover(Mover):
    type = Type.SNAKE

    def _positions_without_block(self, unit: Unit, board):
        print("Snake moves")


class BishopMover(Mover):
    type = Type.BISHOP

    def _positions_without_block(self, unit: Unit, board):
        result = set()
        x, y = board.position_of_unit[unit]
        going = [True] * 4
        for delta in range(1, board.size_map + 1):
            for num, pos in zip(range(4),
                                ((x - delta, y - delta),
                                 (x - delta, y + delta),
                                 (x + delta, y - delta),
                                 (x + delta, y + delta))):
                if 0 <= pos[0] < board.size_map and 0 <= pos[1] < board.size_map:
                    if board[pos] is not None:
                        going[num] = False
                    if going[num]:
                        result.add(pos)
        return result


class RookMover(Mover):
    type = Type.ROOK

    def _positions_without_block(self, unit: Unit, board):
        result = set()
        x, y = board.position_of_unit[unit]
        going = [True] * 4
        for delta in range(1, board.size_map + 1):
            for num, pos in zip(range(4),
                                ((x, y - delta),
                                (x, y + delta),
                                (x - delta, y),
                                (x + delta, y))):
                if 0 <= pos[0] < board.size_map and 0 <= pos[1] < board.size_map:
                    if board[pos] is not None:
                        going[num] = False
                    if going[num]:
                        result.add(pos)

        return result


class SwapMover(Mover):
    type = Type.SWAP

    def _positions_without_block(self, unit: Unit, board):
        print("Vengeful spirit moves")


class PoliceManMover(Mover):
    type = Type.POLICE

    def _positions_without_block(self, unit: Unit, board):
        return KingMover()._positions_without_block(unit, board)


class CheckersKingMover(Mover):
    type = Type.CHECKERS_KING

    def _positions_without_block(self, unit: Unit, board):
        print("Checker King moves")
