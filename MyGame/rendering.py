from MyGame.johnson import getAD
from MyGame.anotation import GameType
from MyGame.utilits.textures import texture
from MyGame.utilits.atlas import FontAtlas
from MyGame.requirements import glm




class TextRender:
    def __init__(self, game: GameType):
        self.game = game

        self.font_atlas = FontAtlas()

        self.ivbo = game.ctx.buffer(reserve=2048)
        self.atlas_texture = texture.create_texture(self.game.ctx, getAD("atlas/fonts.png"), flip_y=False)

        ebo, vbo = game.ebo, game.vbo
        self.program = game.programs.shader_text
        self.vao = game.ctx.vertex_array(self.program, [(vbo, "2f 2f", "inPos", "inUV"), (self.ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=ebo)

        self.Position = glm.vec2(0)
        self.Scale = glm.vec2(100)
        self.SizeAtlas = glm.vec2(8)
        self.Zayer = 1
        self.Alpha = 1

        self.StartX = 0
        self.StartY = 0
        self.SpaceX = 100
        self.SpaceY = 120
        self.NewLineX = 0
        

        self.ColorChange = glm.vec3(1)

       


    def renderText(self, text: str):
        self.atlas_texture.use()

        self.ivbo.write(self.font_atlas.generateTextListByte(text, start_x=self.StartX, start_y=self.StartY, space_x=self.SpaceX, space_y=self.SpaceY, new_line_x=self.NewLineX))

        self.program["unPos"] = self.Position
        self.program["unScale"] = self.Scale
        self.program["unAtlas"] = self.SizeAtlas
        self.program["unZayer"] = self.Zayer
        self.program["color_change"] = self.ColorChange
        self.program["alpha"] = self.Alpha
        self.program["tex"] = 0

        
        self.vao.render(instances=self.font_atlas.instance_count)