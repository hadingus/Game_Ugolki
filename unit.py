import copy
from enum import Enum
from abc import ABC, abstractmethod


class Unit:
    __next_id = 0

    def __init__(self, mover: 'Mover'):
        self.id = Unit.__next_id
        self._mover = mover
        self._type = mover.type
        self._board = None

    def __copy__(self):
        new_unit = self.__class__(self._mover)
        new_unit.__dict__.update(self.__dict__)
        new_unit._mover = copy.copy(self._mover)
        return new_unit

    def __deepcopy__(self, memo={}):
        new_unit = self.__class__(self._mover)
        new_unit.__dict__.update(self.__dict__)
        new_unit._mover = copy.deepcopy(self._mover, memo)
        return new_unit

    def __hash__(self):
        return hash(id)

    def move(self, position):
        if self._board is None:
            raise ValueError('Board is not set')
        self._mover.move(self, self._board, position)

    def set_board(self, board):
        self._board = board

    def set_mover(self, new_mover):
        self._mover = new_mover

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type


class Mover(ABC):
    type = None

    @abstractmethod
    def move(self, unit, board, position):
        pass


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

    def move(self, unit, board, position):
        print("Pawn moves")


class KingMover(Mover):
    type = Type.KING

    def move(self, unit, board, position):
        print("King moves")


class UsualMover(Mover):
    type = Type.USUAL

    def move(self, unit, board, position):
        print("Usual figure moves")


class FlexMover(Mover):
    type = Type.FLEX

    def move(self, unit, board, position):
        print("Flex figure moves")


class SnakeMover(Mover):
    type = Type.SNAKE

    def move(self, unit, board, position):
        print("Snake moves")


class BishopMover(Mover):
    type = Type.BISHOP

    def move(self, unit, board, position):
        print("Bishop moves")


class RookMover(Mover):
    type = Type.ROOK

    def move(self, unit, board, position):
        print("Rook moves")


class SwapMover(Mover):
    type = Type.SWAP

    def move(self, unit, board, position):
        print("Vengeful spirit moves")


class PoliceManMover(Mover):
    type = Type.POLICE

    def move(self, unit, board, position):
        print("Police man moves")


class CheckersKingMover(Mover):
    type = Type.CHECKERS_KING

    def move(self, unit, board, position):
        print("Checker King moves")
