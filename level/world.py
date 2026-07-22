from supermarioworld.typing.gametype import GameType, BasicEvent
from supermarioworld.spatial_hash import ChunkHasher
from supermarioworld.camera import Camera

from level.entities import Block
from level.mario import Mario

class World:
    def __init__(self, game: GameType, biome: int):
        self.game = game
        self.renderer = game.renderer

        self.camera = Camera(self.game.width, self.game.height,smooth=0.05)
        self.camera.setBounds(0, 0, 2000, self.game.height)

        self.spatial_hash = ChunkHasher(cell_sizes=(500, 600))
        self.current_cell = None

        self.entities = []
        self.objects = []


        self.main_entity = Mario(game, world=self) 

        self.game.assets.regCutOutImage("line-1", atlas_key="tiles", x=275, y=80, w=16, h=16)
        self.game.assets.regCutOutImage("b2", atlas_key="tiles", x=444, y=202, w=16, h=16)
        self.game.assets.regCutOutImage("b5", atlas_key="tiles", x=444, y=220, w=16, h=16)


        for x in range(0, 2000, 48):
            block = Block(game)
            block.x = x
            block.y = 500
            block.texture = "b2"
            self.entities.append(block)

        for x in range(0, 2000, 48):
            block = Block(game)
            block.x = x
            block.y = 548
            block.texture = "b5"
            self.entities.append(block)
        

        # Левая стенка
        for y in range(0, 200, 48):
            block = Block(game)
            block.x = 500
            block.y = y
            block.texture = "line-1"
            self.entities.append(block)



        self.spatial_hash.setEntities(self.entities)

        self.objects = self.spatial_hash.getEntities(self.main_entity.x, self.main_entity.y)


    def update(self):
        self.camera.update(self.game.delta_time, target_x=self.main_entity.x, target_y=self.main_entity.y)

        self.main_entity.update(self.game.delta_time)

        cell = self.spatial_hash.getCellSizes(self.main_entity.x, self.main_entity.y)

        if cell != self.current_cell:
            self.objects = self.spatial_hash.getEntities(self.main_entity.x, self.main_entity.y)
            self.current_cell = cell


        for entity in self.objects:
            entity.update(self.game.delta_time)


    def handle(self, event: BasicEvent):
        pass


    def render(self):
        self.game.clearColor(0, 0.7, 0.8)
        bg_width = self.game.width
        factor = 0.3

        offset = -(self.camera.x * factor)
        offset %= bg_width
        offset -= bg_width

        x = offset

        while x < self.game.width:
            self.renderer.render("background", position=(x, 0), size=(bg_width, self.game.height))
            x += bg_width


        for entity in self.objects:
            entity.render(self.camera)

        if self.game.DEBUG:
            self.spatial_hash.renderDebug(self.renderer, self.camera)

        self.main_entity.render(self.camera)

        