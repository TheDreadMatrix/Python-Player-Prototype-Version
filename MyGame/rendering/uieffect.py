from MyGame.scenes_component import GameType
from MyGame.requirements import glm


class FadeEffect:
    def __init__(self, game: GameType):
        self.game = game

        self.program = game._ctx.program(game.paths.ShaderText("vertex/fade.vert"), game.paths.ShaderText("fragment/fade.frag"))
        self.vao = game._ctx.vertex_array(self.program, [(game._vbo_only, "2f", "inPos")], index_buffer=game._ebo)

        self.Position = glm.vec2(0)
        self.Scale = glm.vec2(game.width, game.height)
        self.Zayer = 3


        self.Color = glm.vec3(0)
        self.Alpha = 0
    


    def fadeIn(self, speed: float):

        self.Alpha -= self.game.delta_time * speed
        self.Alpha = glm.clamp(self.Alpha, 0.0, 1.0)


    def fadeOut(self, speed: float):


        self.Alpha += self.game.delta_time * speed
        self.Alpha = glm.clamp(self.Alpha, 0.0, 1.0)


    def renderFadeEffect(self):
        if self.Alpha <= 0.0:
            return

        self.program["unPos"] = self.Position
        self.program["unScale"] = self.Scale
        self.program["unZayer"] = self.Zayer
        self.program["Color"] = self.Color
        self.program["Alpha"] = self.Alpha

        self.vao.render()
