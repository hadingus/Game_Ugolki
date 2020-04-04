from copy import deepcopy
from game_lib import *

someMovers = [PawnMover(), KingMover(), FlexMover(), SwapMover()]

units = []

for i in range(8):
    units.append(Unit(str(i), someMovers[i % 4]))

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

for i in range(8):
    assert units[i].type == units[i + 8].type

print("All is correct")
