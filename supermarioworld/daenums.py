from enum import IntEnum


class TextureFilters(IntEnum):
    NEAREST = 0
    LINEAR = 1
    NEAREST_NEAR = 2
    LINEAR_NEAR = 3
    NEAREST_LINE = 4
    LINEAR_LINE = 5