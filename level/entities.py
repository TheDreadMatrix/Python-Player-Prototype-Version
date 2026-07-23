from supermarioworld.typing.gametype import GameType
from supermarioworld.spatial_hash import ChunkHasher
from typing import TypeVar, Type

T = TypeVar("T", bound="Entity")


class BaseWorld:
    def __init__(self, game: GameType):
        self.game = game
        self.assets = game.assets
        self.renderer = game.renderer

        self.main_entity: "Character" = None

        self.spatial_hash = ChunkHasher(cell_sizes=(500, 600))
        self.current_cell = None

        self.entities: list[Entity] = []
        self.objects: list[Entity] = []

    def show_message(self, text): pass
    def spawn_effect(self, effect: T): pass
    def spawn(self, object: T) -> T: pass


class Entity:
    def __init__(self, world: BaseWorld, x=0, y=0, w=50, h=100, vx=0, vy=0):
        self.world = world
        self.game = world.game
        self.renderer = world.game.renderer
        self.assets = world.game.assets
        self.keyboard = world.game.keyboard


        self.x, self.y = x, y
        self.w, self.h = w, h

        self.vx = vx
        self.vy = vy

        self.gravity = 1200
        self.acceleration = 1200

        self.on_ground = False
        self.solid = False
        self.dead = False
        self.beat = False


    def intersects(self, other: "Entity"):
        return (
            self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y
        )


    def update(self, delta_time: float):
        self.move_x(delta_time)
        self.move_y(delta_time)


    def set_pos(self, x, y):
        self.x = x
        self.y = y
        return self


    def hit_from_below(self, entity: "Entity"): pass
    def move_x(self, delta_time):pass
    def move_y(self, delta_time):pass
    def on_beat(self): pass
    def render(self, camera):pass

    def kill(self): self.dead = True



class Character(Entity):
    def __init__(self, world: BaseWorld):
        super().__init__(world=world)
    
        self.jump_force = -800
        
        self.health = 1

    def set_powerup(self, state: int): pass
    def set_action(self, state: int): pass



class Item(Entity):
    def on_spawn_from_block(self, block: "Block"): pass
    def on_collect(self, player: "Character"): pass
        


class Block(Entity):
    def __init__(self, world: BaseWorld):
        super().__init__(world, w=48, h=48)
        self.texture = None
        self.animation = None

        self.solid = True

    def set_texture(self, texture):
        self.texture = texture
        return self

    def set_animation(self, animation):
        self.animation = animation
        return self

    def render(self, camera):
        x, y = camera.apply(0, 0) 

        if self.animation is not None:
            self.animation.update()
            texture = self.animation.getTextureKey()
        else:
            texture = self.texture

        self.renderer.render(texture, position=(self.x + x, self.y + y), size=(self.w, self.h))


