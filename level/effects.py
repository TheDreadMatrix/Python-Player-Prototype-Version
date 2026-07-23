from supermarioworld.rendering.animation import AnimationCutOut

from level.entities import Entity


class SkidDust(Entity):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, w=32, h=32)
        self.animation = AnimationCutOut(self.game, key_atlas="mario-spr", frames=[(12, 3566, 8, 8), (32, 3566, 8, 8), (52, 3566, 8, 8)], durations=[0.2, 0.2, 0.2], repeat=False)

        self.x = x
        self.y = y
        self.dead = False
        
     

    def update(self, delta_time):
        self.animation.update()
        if self.animation.finished:
            self.kill()

    def render(self, camera):
        x, y = camera.apply(self.x, self.y)
        self.renderer.render(self.animation.getTextureKey(), position=(x, y), size=(self.w, self.h))