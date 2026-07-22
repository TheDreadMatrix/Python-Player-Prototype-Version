from supermarioworld.typing.gametype import GameType



class Entity:
    def __init__(self, game: GameType, x=0, y=0, w=50, h=100):
        self.renderer = game.renderer
        self.assets = game.assets
        self.keyboard = game.keyboard


        self.x, self.y = x, y
        self.w, self.h = w, h


    def intersects(self, other: "Entity"):
        return (
            self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y
        )


    def update(self, delta_time: float):
        pass


    def move_x(self, delta_time):
        pass


    def move_y(self, delta_time):
        pass


    def render(self, camera):
        pass

    def kill(self):
        pass



class Character(Entity):
    def __init__(self, game: GameType):
        super().__init__(game=game)

        self.speed = 250
        self.jump_force = -800
        self.gravity = 1200

        self.health = 1
        self.on_ground = False


        self.vx = 0
        self.vy = 0

    def update(self, delta_time):
        self.move_x(delta_time)
        self.move_y(delta_time)


class Block(Entity):
    def __init__(self, game):
        super().__init__(game, w=48, h=48)
        self.texture = None
        self.animation = None


    def render(self, camera):
        x, y = camera.apply(0, 0) 

        if self.animation is not None:
            self.animation.update()
            texture = self.animation.getTextureKey()
        else:
            texture = self.texture

        self.renderer.render(texture, position=(self.x + x, self.y + y), size=(self.w, self.h))

