from supermarioworld.typing.gametype import GameType, BasicEvent

from supermarioworld.camera import Camera

from supermarioworld.rendering.animation import AnimationCutOut
from supermarioworld.rendering.users import TextLabel

from level.entities import Block, BaseWorld
from level.blocks import LootBlock, MessageBlock
from level.items import Mushroom
from level.mario import Mario

class World(BaseWorld):
    def __init__(self, game: GameType, biome: int, time=3):
        super().__init__(game)
        self.time = time

        self.time_label = TextLabel(game, f"TIME: {self.time}", font_key="pixel")
        self.time_label.position = (500, 50)

        self.main_entity = Mario(world=self) 

        self.camera = Camera(self.game.width, self.game.height,smooth=0.05)
        self.camera.setBounds(0, 0, 2000, self.game.height)

        


        

        self.assets.regCutOutImage("line-1", atlas_key="tiles", x=275, y=80, w=16, h=16)
        self.assets.regCutOutImage("b2", atlas_key="tiles", x=444, y=202, w=16, h=16)
        self.assets.regCutOutImage("b5", atlas_key="tiles", x=444, y=220, w=16, h=16)
        self.assets.regCutOutImage("used-block", atlas_key="tiles", x=257, y=97, w=16, h=16)

        anim = AnimationCutOut(game, key_atlas="tiles", frames=[(173, 181, 16, 16), (190, 181, 16, 16), (207, 181, 16, 16), (224, 181, 16, 16)], durations=[0.12])


        block = LootBlock(self, Mushroom)
        block.x = 192
        block.y = 300
        block.animation = anim
        self.entities.append(block)


        mushroom = Mushroom(world=self, x=600, y=-152)
        self.entities.append(mushroom)

        self.entities.append(Block(self).set_pos(192, 452).set_texture("line-1"))
        self.entities.append(Block(self).set_pos(500, 452).set_texture("line-1"))
        self.entities.append(MessageBlock(self, text="Hello fellow").set_pos(452, 192).set_texture("line-1"))

        for x in range(0, 2000, 48):
            block = Block(self).set_pos(x, 500).set_texture("b2")
            self.entities.append(block)

        for x in range(0, 2000, 48):
            block = Block(self).set_pos(x, 548).set_texture("b5")
            self.entities.append(block)
        

        # Левая стенка
        for y in range(0, 200, 48):
            block = Block(self)
            block.x = 500
            block.y = y
            block.texture = "line-1"
            self.entities.append(block)



        
        self.spatial_hash.setEntities(self.entities)
        self.objects = self.spatial_hash.getEntities(self.main_entity.x, self.main_entity.y)


    def spawn(self, object):
        self.entities.append(object)
        self.spatial_hash.setEntities(self.entities)
        self.objects = self.spatial_hash.getEntities(self.main_entity.x, self.main_entity.y)

        return object


    def spawn_effect(self, effect):
        self.objects.append(effect)


    def update(self):
        self.time -= self.game.delta_time
        self.time_label.setText(f"TIME: {int(self.time)}")

        self.camera.update(self.game.delta_time, target_x=self.main_entity.x, target_y=self.main_entity.y)

        self.main_entity.update(self.game.delta_time)

        if self.main_entity.beat:
            self.main_entity.on_beat()


        cell = self.spatial_hash.getCellSizes(self.main_entity.x, self.main_entity.y)

        if cell != self.current_cell:
            self.objects = self.spatial_hash.getEntities(self.main_entity.x, self.main_entity.y)
            self.current_cell = cell


        for entity in self.objects[:]:
            entity.update(self.game.delta_time)

            if entity.dead:
                self.objects.remove(entity)

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

        if self.game.DEBUG:
            self.spatial_hash.renderDebug(self.renderer, self.camera)

        self.main_entity.render(self.camera)


        self.time_label.render()



        