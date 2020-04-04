from copy import deepcopy
from game_lib import *
from gamemode import *

someMovers = [PawnMover(), KingMover(), FlexMover(), SwapMover()]

units = []

for i in range(8):
    units.append(Unit(someMovers[i % 4]))

for unit in units:
    unit.move(None, None)

# Hash test

unitSet = set(units)
print("Len of set", len(units))

# Copying

for i in range(8):
    units.append(deepcopy(units[i]))

unitSet = set(units)
print("Len of double set", len(units))

print("All is correct")

# GameMode Test

dir = Director()
b = (ClassicModeBuilder(), AdvancedModeBuilder(), TriangleModeBuilder(),
                            AllUnitsModeBuilder(), KingPoliceModeBuilder(), WallModeBuilder())

modes = [dir.construct_game_mode(md) for md in b]
for m in modes:
    print(m.size_map)

print("GameMode is correct")



