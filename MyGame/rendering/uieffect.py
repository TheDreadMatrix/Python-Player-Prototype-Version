from MyGame.scenes_component import GameType
from MyGame.requirements import glm


class FadeEffect:
    def __init__(self, game: GameType):
        self.game = game

        self.program = game._ctx.program()
        self.vao = game._ctx.vertex_array()


        self.Color = glm.vec3(0)
        self.Alpha = 0


    def fadeIn(self):
        pass


    def fadeOut(self):
        pass


    def renderFadeEffect(self):
        pass