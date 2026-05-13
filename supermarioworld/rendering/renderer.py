from supermarioworld.rendering.custom_shaders import CustomShader
from supermarioworld.rendering.moderngl import create_error_texture

class Sprite2D:
    def __init__(self, game, custom_shader: CustomShader|None=None):
        self.game = game

        self.position = (0, 0)
        self.size = (100, 100)

        self.layer = 1
        self.flip_x = False
        self.flip_y = False

        self.texture = create_error_texture(game._ctx)

        self._program = game._ctx.program(CustomShader._DEFAULT_VERTEX_SOURCE, CustomShader._DEFAULT_FRAGMENT_SOURCE) if not custom_shader else custom_shader._program
        self._vao = game._ctx.vertex_array(self._program, [(self.game._vbo, "2f 2f", "inPos", "inCoord")], index_buffer=self.game._ebo)


    def render(self):
        self.texture.use()

        self._program["unPos"] = self.position
        self._program["unSize"] = self.size
        self._program["unLayer"] = self.layer
        self._program["unFlx"] = self.flip_x
        self._program["unFly"] = self.flip_y

        self._program["DM_Texture"] = 0

        self._vao.render()



    


