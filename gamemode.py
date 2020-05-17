from abc import ABC, abstractmethod
from unit import Unit, UsualMover, FlexMover, CheckersKingMover, PoliceManMover, SwapMover, SnakeMover
from unit import RookMover, BishopMover, KingMover, PawnMover
from enum import Enum


class ModeFeature(Enum):
    AI = 1


class GameMode:

    def __init__(self):
        self.size_map = 0
        self.arrangement = []
        self.features = set()
        self.name = ""

    def __init__(self, size, arrangement):
        self.size_map = size
        self.arrangement = arrangement
        self.features = set()
        self.name = ""


class GameModeBuilder(ABC):

    _base_map_size = 8
    _mod_name = "Имя по умолчанию"

    def __init__(self):
        self.reset()

    def reset(self):
        self._result = GameMode()

    def get_result(self):
        result = self._result
        self.reset()
        return result

    def set_name(self):
        self._result.name = self._mod_name

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


class FlexSquareBuilder(SquareBuilder):
    _width = 3
    _height = 3
    _mod_name = "Диагональные уголки 3x3"

    def set_size(self):
        self._result.size_map = SquareBuilder._base_map_size

    def set_arrangement(self):
        _unit_list = []
        for i in range(self._width * self._height):
            _unit_list.append(Unit(FlexMover()))
        self.put_units(self._width, self._height, _unit_list)


class UsualUnitBuilder(SquareBuilder, ABC):
    def set_size(self):
        self._result.size_map = SquareBuilder._base_map_size

    def set_arrangement(self):
        _unit_list = []
        for i in range(self._width * self._height):
            _unit_list.append(Unit(UsualMover()))
        self.put_units(self._width, self._height, _unit_list)


class ClassicModeBuilder(UsualUnitBuilder):
    _width = 3
    _height = 3
    _mod_name = "Классические уголки 3x3"


class AdvancedModeBuilder(UsualUnitBuilder):
    _width = 3
    _height = 4
    _mod_name = "Классические уголки 3x4"


class TriangleModeBuilder(GameModeBuilder):

    def set_size(self):
        self._result.size_map = self._base_map_size

    def set_arrangement(self):
        for i in range(4):
            for j in range(4 - i):
                self._result.arrangement.append(
                        (Unit(FlexMover()), i, j))


class AllUnitsModeBuilder(GameModeBuilder):
    _mod_name = "Мешанина"

    def set_size(self):
        self._result.size_map = 9

    def set_arrangement(self):
        self._result.arrangement.append((Unit(CheckersKingMover()), 0, 0))
        self._result.arrangement.append((Unit(PoliceManMover()), 0, 1))
        self._result.arrangement.append((Unit(SwapMover()), 1, 0))
        self._result.arrangement.append((Unit(SnakeMover()), 1, 1))
        self._result.arrangement.append((Unit(RookMover()), 0, 2))
        self._result.arrangement.append((Unit(BishopMover()), 0, 3))
        self._result.arrangement.append((Unit(FlexMover()), 1, 2))
        self._result.arrangement.append((Unit(UsualMover()), 2, 1))
        self._result.arrangement.append((Unit(KingMover()), 2, 0))
        self._result.arrangement.append((Unit(PawnMover()), 3, 0))


class KingPoliceModeBuilder(SquareBuilder):
    _mod_name = "Короли и полицейские"

    def set_size(self):
        self._result.size_map = 15

    def set_arrangement(self):
        _unit_list = []
        for i in range(4):
            _unit_list.append(Unit(KingMover()))
        _unit_list.append(Unit(PoliceManMover()))
        for i in range(4):
            _unit_list.append(Unit(KingMover()))
        self.put_units(3, 3, _unit_list)


class WallModeBuilder(SquareBuilder):
    _mod_name = "Стенка на стенку"

    def set_size(self):
        self._result.size_map = 15

    def set_arrangement(self):
        _unit_list = []
        for i in range(4):
            _unit_list.append(Unit(BishopMover()))
            _unit_list.append(Unit(RookMover()))
        _unit_list.append(Unit(BishopMover()))
        self.put_units(3, 3, _unit_list)


class Director:
    def construct_game_mode(self, builder: GameModeBuilder):
        builder.reset()
        builder.set_size()
        builder.set_arrangement()
        builder.set_name()
        return builder.get_result()


class AiDecorator(GameMode):
    def __init__(self, gamemode: GameMode, ai):
        self.wrappee = gamemode
        self.size_map = gamemode.size_map
        self.arrangement = gamemode.arrangement
        self.features = gamemode.features
        self.features.add(ModeFeature.AI)
        self.ai = ai
