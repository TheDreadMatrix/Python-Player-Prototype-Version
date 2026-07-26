from enum import IntEnum

class TextureFilter(IntEnum):
    NEAREST = 0
    LINEAR = 1
    NEAREST_NEAR = 2
    LINEAR_NEAR = 3
    NEAREST_LINE = 4
    LINEAR_LINE = 5


class Anisotropy(IntEnum):
    X0 = 0
    X1 = 1
    X2 = 2
    X4 = 4
    X8 = 8
    X16 = 16


class RenderMode(IntEnum):
    TRIANGLES = 0
    LINE_LOOP = 1
    LINE_STRIP = 2
    POINTS = 3
    TRIANGLE_FAN = 4