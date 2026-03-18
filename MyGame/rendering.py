from MyGame.anotation import GameType






class TextRender:
    def __init__(self, game: GameType):
        self.game = game

        self.ivbo = game.ctx.buffer(reserve=2048)

        ebo, vbo = game.ebo, game.vbo
        self.program = game.programs.shader_text
        self.vao = game.ctx.vertex_array(self.program, [vbo, "2f 2f", game.programs.GLSL.IN_POS, game.programs.GLSL.IN_UV], index_buffer=ebo)


    def renderText(self, text: str):
        pass