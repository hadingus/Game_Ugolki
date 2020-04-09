from abc import ABC, abstractmethod
import unit


class GameMode:

    def __init__(self):
        self.size_map = 0
        self.arrangement = []


class GameModeBuilder(ABC):

    def __init__(self):
        self.reset()

    def reset(self):
        self._result = GameMode()

    def get_result(self):
        result = self._result
        self.reset()
        return result

    @abstractmethod
    def set_size(self):
        pass

    @abstractmethod
    def set_arrangement(self):
        pass


class SquareBuilder(GameModeBuilder, ABC):

    def put_units(self, n, m, _unit_list):
        k = 0
        for i in range(n):
            for j in range(m):
                self._result.arrangement.append((_unit_list[k], i, j))
                k += 1


class ClassicModeBuilder(SquareBuilder):

    def set_size(self):
        self._result.size_map = 8

    def set_arrangement(self):
        _unit_list = []
        for i in range(9):
            _unit_list.append(unit.Unit(unit.UsualMover()))
        self.put_units(3, 3, _unit_list)


class AdvancedModeBuilder(SquareBuilder):

    def set_size(self):
        self._result.size_map = 8

    def set_arrangement(self):
        _unit_list = []
        for i in range(12):
            _unit_list.append(unit.Unit(unit.UsualMover()))
        self.put_units(3, 4, _unit_list)


class TriangleModeBuilder(GameModeBuilder):

    def set_size(self):
        self._result.size_map = 8

    def set_arrangement(self):
        for i in range(4):
            for j in range(4 - i):
                self._result.arrangement.append(
                        (unit.Unit(unit.FlexMover()), i, j))


class AllUnitsModeBuilder(GameModeBuilder):

    def set_size(self):
        self._result.size_map = 9

    def set_arrangement(self):
        self._result.arrangement.append((unit.Unit(unit.CheckersKingMover()), 0, 0))
        self._result.arrangement.append((unit.Unit(unit.PoliceManMover()), 0, 1))
        self._result.arrangement.append((unit.Unit(unit.SwapMover()), 1, 0))
        self._result.arrangement.append((unit.Unit(unit.SnakeMover()), 1, 1))
        self._result.arrangement.append((unit.Unit(unit.RookMover()), 0, 2))
        self._result.arrangement.append((unit.Unit(unit.BishopMover()), 0, 3))
        self._result.arrangement.append((unit.Unit(unit.FlexMover()), 1, 2))
        self._result.arrangement.append((unit.Unit(unit.UsualMover()), 2, 1))
        self._result.arrangement.append((unit.Unit(unit.KingMover()), 2, 0))
        self._result.arrangement.append((unit.Unit(unit.PawnMover()), 3, 0))


class KingPoliceModeBuilder(SquareBuilder):

    def set_size(self):
        self._result.size_map = 15

    def set_arrangement(self):
        _unit_list = []
        for i in range(4):
            _unit_list.append(unit.Unit(unit.KingMover()))
        _unit_list.append(unit.Unit(unit.PoliceManMover()))
        for i in range(4):
            _unit_list.append(unit.Unit(unit.KingMover()))
        self.put_units(3, 3, _unit_list)


class WallModeBuilder(SquareBuilder):

    def set_size(self):
        self._result.size_map = 15

    def set_arrangement(self):
        _unit_list = []
        for i in range(4):
            _unit_list.append(unit.Unit(unit.BishopMover()))
            _unit_list.append(unit.Unit(unit.RookMover()))
        _unit_list.append(unit.Unit(unit.BishopMover()))
        self.put_units(3, 3, _unit_list)


class Director:
    def construct_game_mode(self, builder):
        builder.reset()
        builder.set_size()
        builder.set_arrangement()
        return builder.get_result()
