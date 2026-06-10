from enum import IntEnum

class TextureFilter(IntEnum):
    NEAREST = 0
    LINEAR = 1
    NEAREST_NEAR = 2
    LINEAR_NEAR = 3
    NEAREST_LINE = 4
    LINEAR_LINE = 5


class RenderMode(IntEnum):
    TRIANGLES = 0
    LINE_LOOP = 1
    LINE_STRIP = 2
    POINTS = 3
    TRIANGLE_FAN = 4