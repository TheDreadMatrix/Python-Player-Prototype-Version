from supermarioworld.typing.gametype import GameType, BasicEvent

from supermarioworld.camera import Camera

from supermarioworld.animation import AnimationCutOut

from level.tilemap import LevelTileMap


from level.entities import Block, BaseWorld
from level.blocks import LootBlock, MessageBlock, SpringBlock, NotSolidBlock
from level.items import Mushroom
from level.mario import Mario

class World(BaseWorld):
    def __init__(self, game: GameType, biome: int, time=299):
        super().__init__(game, time=time)


        self.main = Mario(world=self) 

        self.camera = Camera(self.game.width, self.game.height,smooth=0.05)
        self.camera.setBounds(0, 0, 2000, self.game.height)

        

        self.assets.regCutOutImage("line-1", atlas_key="tiles", x=275, y=80, w=16, h=16)
        self.assets.regCutOutImage("b2", atlas_key="tiles", x=444, y=202, w=16, h=16)
        self.assets.regCutOutImage("b5", atlas_key="tiles", x=444, y=220, w=16, h=16)
        self.assets.regCutOutImage("used-block", atlas_key="tiles", x=257, y=97, w=16, h=16)

        anim = AnimationCutOut(game, key_atlas="tiles", frames=[(173, 181, 16, 16), (190, 181, 16, 16), (207, 181, 16, 16), (224, 181, 16, 16)], durations=[0.12])
        ansp = AnimationCutOut(game, key_atlas="tiles", 
                               frames=[(173, 147, 16, 16), (190, 147, 16, 16), (207, 147, 16, 16), (224, 147, 16, 16), 
                                        (224, 147, 16, 16), (207, 147, 16, 16), (190, 147, 16, 16), (173, 147, 16, 16),], 
                                       durations=[0.3])

        block = SpringBlock(self)
        block.x = 192
        block.y = 300
        block.animation = ansp
        self.spawn_block(block)


        mushroom = Mushroom(world=self, x=600, y=-152)
        self.spawn(mushroom)

        self.spawn_block(Block(self).set_pos(192, 452).set_texture("line-1"))
        self.spawn_block(NotSolidBlock(self).set_pos(500, 452).set_texture("line-1"))
        self.spawn_block(MessageBlock(self, text="Hello fellow").set_pos(452, 192).set_texture("line-1"))

        for x in range(0, 2000, 48):
            block = Block(self).set_pos(x, 500).set_texture("b2")
            self.spawn_block(block)

        for x in range(0, 2000, 48):
            block = Block(self).set_pos(x, 548).set_texture("b5")
            self.spawn_block(block)
        
        


    def spawn_block(self, block):
        self.statics.append(block)
        self.spatial_hash.set_entity(block)
        self.objects = self.spatial_hash.getEntities(self.main.x, self.main.y)

        return block


    def spawn_effect(self, effect):
        self.objects.append(effect)

    def spawn(self, entity):
        self.dynamics.append(entity)
        return entity


    def update(self):
        if not self.main.beat:
            super().update()
        

        self.camera.update(self.game.delta_time, target_x=self.main.x, target_y=self.main.y)



        self.main.update(self.game.delta_time)

        if self.main.beat:
            self.main.on_beat()


        cell = self.spatial_hash.getCellSizes(self.main.x, self.main.y)

        if cell != self.current_cell and not self.main.beat:
            self.objects = self.spatial_hash.getEntities(self.main.x, self.main.y)
            self.current_cell = cell


        for entity in self.objects[:]:
            entity.update(self.game.delta_time)

            if entity.dead:
                self.objects.remove(entity)

            if entity.beat:
                entity.on_beat()


        for entity in self.dynamics[:]:
            entity.update(self.game.delta_time)

            if entity.dead:
                self.dynamics.remove(entity)

            if entity.beat:
                entity.on_beat()

       


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

        for entity in self.dynamics:
            entity.render(self.camera)

        if self.game.DEBUG:
            self.spatial_hash.renderDebug(self.renderer, self.camera)

        self.main.render(self.camera)


        



        