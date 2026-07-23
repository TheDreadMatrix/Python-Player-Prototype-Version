from enum import IntEnum


class CharacterPowerup(IntEnum):
    SMALL = 0
    SUPER = 1
    FIRE = 2
    CAPE = 3
    

class CharacterEnvironment(IntEnum):
    GROUND = 0
    WATER = 1


class CharacterAction(IntEnum):
    IDLE = 0
    WALK = 1
    RUN = 2
    JUMP = 3
    SWIM = 4
    DROWN = 5
    FALL = 6
    DUCK = 7
    SKID = 8
    LOOK_UP = 9
    RUN_JUMP = 10
    SPIN = 11
    DEAD = 12




class CharacterStarup(IntEnum):
    NORMAL = 0
    STAR = 1