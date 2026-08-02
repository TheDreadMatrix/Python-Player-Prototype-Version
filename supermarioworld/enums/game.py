from enum import IntEnum






class LevelBiome(IntEnum):
    VALLEY = 0
    UNDERGROUND = 1
    RED_FOREST = 2
    CASTLE = 3


class OverWorldBiome(IntEnum):
    VALLEY = 0
    UNDERGROUND = 1
    RED_FOREST = 2
    MAGMA = 3
    SPECIAL = 4



class CollisionType(IntEnum):
    SOLID = 0
    SLOPE_LEFT = 1
    SLOPE_RIGHT = 2