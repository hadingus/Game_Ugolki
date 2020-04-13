from unit import Type
from itertools import product

from gamemode import Director, ClassicModeBuilder, AllUnitsModeBuilder


def test_classic():
    director = Director()
    mode = director.construct_game_mode(ClassicModeBuilder())

    assert mode.size_map == 8

    positions = set()

    for unit, x, y in mode.arrangement:
        assert 0 <= x < 3 and 0 <= y < 3
        assert unit.type == Type.USUAL
        positions.add((x, y))

    print(len(positions))
    assert len(positions) == 9
