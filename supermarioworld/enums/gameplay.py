from enum import IntEnum

REDIRECT_TO_OVERWORLD = 0


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