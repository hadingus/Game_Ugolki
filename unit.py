import copy
from abc import ABC, abstractmethod


class Unit:
    __next_id = 0

    def __init__(self, mover):
        self.id = Unit.__next_id
        self._mover = mover

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

    def move(self, board, position):
        self._mover.move(self, board, position)


class Mover(ABC):
    @abstractmethod
    def move(self, unit, board, position):
        pass


class PawnMover(Mover):
    def move(self, unit, board, position):
        print("Pawn moves")


class KingMover(Mover):
    def move(self, unit, board, position):
        print("King moves")


class UsualMover(Mover):
    def move(self, unit, board, position):
        print("Usual figure moves")


class FlexMover(Mover):
    def move(self, unit, board, position):
        print("Flex figure moves")


class SnakeMover(Mover):
    def move(self, unit, board, position):
        print("Snake moves")


class BishopMover(Mover):
    def move(self, unit, board, position):
        print("Bishop moves")


class RookMover(Mover):
    def move(self, unit, board, position):
        print("Rook moves")


class SwapMover(Mover):
    def move(self, unit, board, position):
        print("Vengeful spirit moves")


class PoliceManMover(Mover):
    def move(self, unit, board, position):
        print("Police man moves")


class CheckersKingMover(Mover):
    def move(self, unit, board, position):
        print("Checker King moves")
