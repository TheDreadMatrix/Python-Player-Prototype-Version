from enum import IntEnum


REDIRECT_TO_OVERWORLD = 100

class TextureFilters(IntEnum):
    NEAREST = 0
    LINEAR = 1
    NEAREST_NEAR = 2
    LINEAR_NEAR = 3
    NEAREST_LINE = 4
    LINEAR_LINE = 5


class RenderModes(IntEnum):
    TRIANGLES = 0
    LINE_LOOP = 1
    LINE_STRIP = 2
    POINTS = 3
    TRIANGLE_FAN = 4


class CharacterState(IntEnum):
    DEFAULT = 0
    POWERUP = 1
    FILEFLOW = 2
    CAPE = 4


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


class Keys(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3


class Mouses(IntEnum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2