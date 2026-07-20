from dataclasses import dataclass


@dataclass(slots=True)
class TileEntity:
    tile: str
    x: float
    y: float 
    s_w: float
    s_h: float
    flx: bool
    fly: bool

EMPTY = ()


class ChunkHasher:
    def __init__(self, cell_sizes: tuple=(128, 128)):
        self.cell_width = cell_sizes[0]
        self.cell_height = cell_sizes[1]
        self.grids = {}

    def getCellSizes(self, x, y):
        return int(x // self.cell_width), int(y // self.cell_height)

    def setEntities(self, entities: list[TileEntity]):
        self.grids.clear()

        cw = self.cell_width
        ch = self.cell_height

        for entity in entities:
            cx = int(entity.x // cw)
            cy = int(entity.y // ch)

            cell = (cx, cy)

            if cell not in self.grids:
                self.grids[cell] = []

            self.grids[cell].append(entity)


    def getEntities(self, x, y):
        cx, cy = self.getCellSizes(x, y)

        entities = []

        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                entities.extend(
                    self.grids.get((cx + ox, cy + oy), EMPTY)
                )

        return entities








