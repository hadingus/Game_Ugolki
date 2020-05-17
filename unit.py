import copy
from enum import Enum
from abc import ABC, abstractmethod
from player import Player
from itertools import product
import numpy as np


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

    def move(self, position):
        if self._board is None:
            raise ValueError('Board is not set')
        return self._mover.move(self, self._board, position)

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

    def move(self, unit: Unit, board, position):
        if not self._initial_checks(unit, board, position):
            return False
        if not self._can_move_to(unit, board, position):
            return False
        start_position = board.position_of_unit[unit]
        board.force_move(start_position, position)
        return True

    def _can_move_to(self, unit, board, position):
        start_position = board.position_of_unit[unit]
        positions = self._possible_positions(unit, board)
        if position in positions:
            return True
        return False

    def _possible_positions(self, unit: Unit, board):
        if not self._able_to_move(unit, board):
            return {}
        return self._positions_without_block(unit, board)

    def _initial_checks(self, unit, board, position):
        size = board.size_map
        return self._check_border(position, size) and board[position] is None

    def _able_to_move(self, unit: Unit, board):
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

    def _check_border(self, position, size):
        return 0 <= position[0] < size and 0 <= position[1] < size

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

    def get_jumps(self, position, board):
        x, y = position
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        result = []
        for dx, dy in delta:
            nx, ny = x + dx, y + dy
            mx, my = x + 2 * dx, y + 2 * dy
            if not self._check_border((nx, ny), board.size_map):
                continue
            if not self._check_border((mx, my), board.size_map):
                continue
            if board[nx, ny] is not None and board[mx, my] is None:
                result.append((mx, my))
        return result

    def _positions_without_block(self, unit: Unit, board):
        result = []
        result.extend(PawnMover()._positions_without_block(unit, board))
        result.extend(Jumper(self).get_positions_by_jump(unit, board))
        return result


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

    def move(self, unit, board, position):
        start_position = board.position_of_unit[unit]
        if start_position == position or not self._check_border(position, board.size_map):
            return False
        if position in self._possible_positions(unit, board):
            board.force_swap(start_position, position)
            return True


    def _positions_without_block(self, unit: Unit, board):
        result = []
        position = board.position_of_unit[unit]
        for x, y in product(range(board.size_map), range(board.size_map)):
            if board[x, y] is not None and position != (x, y):
                result.append((x, y))

        return result


class PoliceManMover(Mover):
    type = Type.POLICE

    def _positions_without_block(self, unit: Unit, board):
        return KingMover()._positions_without_block(unit, board)


class CheckersKingMover(Mover):
    type = Type.CHECKERS_KING

    def _positions_without_block(self, unit: Unit, board):
        result = []
        position = board.position_of_unit[unit]
        for x, y in product(range(board.size_map), range(board.size_map)):
            if board[x, y] is None and position != (x, y):
                result.append((x, y))

        return result


class Jumper:
    def __init__(self, mover):
        self._mover = mover

    def get_positions_by_jump(self, unit: Unit, board):
        position = board.position_of_unit[unit]
        size = board.size_map

        used = np.zeros(shape=(size, size))
        result = []

        def dfs(pos):
            if used[pos]:
                return
            used[pos] = True
            result.append(pos)
            for step in self._mover.get_jumps(pos, board):
                dfs(step)

        dfs(position)
        return result
