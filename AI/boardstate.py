import numpy as np
from typing import Optional, List
from itertools import product


class BoardState:
    width = 8
    height = 8

    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    @staticmethod
    def _get_empty_board(y, x):
        return np.zeros((y, x), dtype=np.int8)

    def __eq__(self, other):
        if other is None:
            return False
        return (self.board == other.board).min() and self.current_player == other.current_player

    def __repr__(self):
        rows = []
        for i in range(self.height):
            rows.append(' '.join(map(lambda x: '+' if x == 1 else '-' if x == -1 else '.', self.board[i])))
        return f'Current player: {self.current_player}\n' + '\n'.join(rows)

    def next_player(self):
        self.current_player *= -1

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, from_y, from_x, to_y, to_x) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        if from_x == to_x and from_y == to_y:
            return None #invalid move

        if self.board[from_y, from_x] * self.current_player <= 0:
            return None

        if self.board[to_y, to_x] != 0:
            return None

        result = self.copy()
        result.board[to_y, to_x] = result.board[from_y, from_x]
        result.board[from_y, from_x] = 0
        result.next_player()
        if result not in self.possible_moves:
            return None

        return result

    @property
    def possible_moves(self) -> List['BoardState']:
        result = []
        for x, y in product(range(self.width), range(self.height)):
            if self.board[y, x] == self.current_player:
                new_moves = self._get_possible_moves_with(y, x)
                for move in new_moves:
                    if self.get_diff(self, move) is not None:
                        result.append(move)
        return result

    def _get_possible_moves_with(self, y, x):
        result = []
        self.next_player()
        self._dfs_brute_force(y, x, result)
        self.next_player()
        return result

    def _dfs_brute_force(self, y, x, result, first_jump=True, used=None):
        if first_jump:
            used = self._get_empty_board(self.height, self.width)
            for ny, nx in product(range(max(0, y - 1), min(self.height, y + 2)),
                                  range(max(0, x - 1), min(self.width, x + 2))):

                if (nx, ny) == (x, y):
                    continue
                if self.board[ny, nx] == 0:
                    self._simple_move(y, x, ny, nx)
                    result.append(self.copy())
                    self._simple_move(ny, nx, y, x)

        for ny, nx in product(range(y - 2, y + 3, 2), range(x - 2, x + 3, 2)):
            if (nx, ny) == (x, y):
                continue
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if used[ny, nx] == 1:
                continue

            if self.board[ny, nx] == 0 and self.board[(y + ny) // 2, (x + nx) // 2] != 0:
                self._simple_move(y, x, ny, nx)
                result.append(self.copy())
                used[ny, nx] = 1
                self._dfs_brute_force(ny, nx, result, False, used)
                self._simple_move(ny, nx, y, x)

    def _simple_move(self, y, x, ny, nx):
        self.board[ny, nx] = self.board[y, x]
        self.board[y, x] = 0

    @property
    def is_game_finished(self) -> bool:
        return self._is_finished_and_winner != 2

    @property
    def _is_finished_and_winner(self) -> int:
        """
        Win if corner filled.
        If white filled corner black has extra step.
        If both field than draw
        1 white wins
        -1 black wins
        0 draw
        2 game continues
        """

        black_finished = self._is_corner_finished
        white_finished = self.inverted()._is_corner_finished

        if white_finished and black_finished:
            return 0

        if black_finished:
            return -1

        if self.current_player == -1 and white_finished:
            for state in self.possible_moves:
                if state._is_corner_finished:
                    return 2

        if white_finished:
            return 1

        return 2

    @property
    def _is_corner_finished(self) -> bool:
        for x, y in product(range(3), range(3)):
            if self.board[y, x] != -1:
                return False
        return True

    @property
    def winner(self) -> Optional[int]:
        if not self.is_game_finished:
            raise Exception("Cannot determine winner. Game is on")
        return self._is_finished_and_winner

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(BoardState.height, BoardState.width), dtype=np.int8)
        return BoardState(board, 1)

    @staticmethod
    def game_state() -> 'BoardState':
        board = np.zeros(shape=(BoardState.height, BoardState.width), dtype=np.int8)
        for x, y in product(range(3), range(3)):
            board[y, x] = 1

        for x, y in product(range(BoardState.width - 3, BoardState.width),
                            range(BoardState.height - 3, BoardState.height)):
            board[y, x] = -1
        return BoardState(board, 1)

    @staticmethod
    def get_diff(board1, board2):
        answer = [-1, -1, -1, -1]
        for x, y in product(range(BoardState.width), range(BoardState.height)):
            if board1.board[x, y] != board2.board[x, y]:
                if board1.board[x, y] == 0:
                    answer[0:2] = (x, y)
                else:
                    answer[2:4] = (x, y)
        if answer[0] == -1:
            return None
        return answer