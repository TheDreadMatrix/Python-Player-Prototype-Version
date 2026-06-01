


class ChunkHasher:
    def __init__(self, cell_sizes: tuple=(128, 128)):
        self.cell_width = cell_sizes[0]
        self.cell_height = cell_sizes[1]
        self.grids = {}

    def getCellSizes(self, x, y):
        return int(x // self.cell_width), int(y // self.cell_height)

    def setEntities(self, entities: list):
        self.grids.clear()

        for entity in entities:
            cx = int(entity.x // self.cell_width)
            cy = int(entity.y // self.cell_height)

            cell = (cx, cy)

            if cell not in self.grids:
                self.grids[cell] = []

            self.grids[cell].append(entity)


    def getEntities(self, x, y):
        cx = int(x // self.cell_width)
        cy = int(y // self.cell_height)

        entities = []

        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                entities.extend(
                    self.grids.get((cx + ox, cy + oy), [])
                )

        return entities






class SpatialHash:
    def __init__(self, cell_size=16):
        self.cell_size = max(1, int(cell_size))
        self.grids = {}


    def setEntities(self, entities: list):
        self.grids.clear()
        cs = self.cell_size
        for e in entities:
            gx = int(e["x"]) // cs
            gy = int(e["y"]) // cs
            self.grids.setdefault((gx, gy), []).append(e)


    def getEntities(self, x, y, rad_x, rad_y):
        cs = self.cell_size
        min_x = int(x - rad_x) // cs
        max_x = int(x + rad_x) // cs
        min_y = int(y - rad_y) // cs
        max_y = int(y + rad_y) // cs
        out = []
        for gy in range(min_y, max_y + 1):
            for gx in range(min_x, max_x + 1):
                out.extend(self.grids.get((gx, gy), ()))
        return out

