from MyGame.anotation import GameType
from MyGame.utilits.atlas import FontAtlas
from MyGame.requirements import glm, mgl, Image



def load_texture(ctx: mgl.Context, path: str):
    img = Image.open(path).convert("RGBA")

    width, height = img.size
    img_data = img.tobytes()

    texture = ctx.texture((width, height), 4, img_data)
    texture.build_mipmaps()
    texture.filter = (mgl.NEAREST, mgl.NEAREST)

    return texture


class CustomShader:
    _VERTEX_HEADER = """#version 330 core\nin vec2 GclUv;\nout vec4 GclColor;\nuniform sampler2D GclTexture;"""
    def __init__(self, game: GameType, shader_filename: str):
        source = game.paths.ShaderText(f"fragment/{shader_filename}")

        pragma = None
        include_vertex = False
        vertex_marker = "__VERTEX_HEADER__"

        lines = source.splitlines()
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("#include"):
                parts = stripped.split()
                if len(parts) >= 2:
                    include_name = parts[1].strip('"')
                    if include_name in ("vertex", "vertex.vert"):
                        include_vertex = True
                        cleaned_lines.append(vertex_marker)
                continue

            if stripped.startswith("#pragma"):
                parts = stripped.split(maxsplit=1)
                if len(parts) > 1:
                    pragma = parts[1].strip().strip('"')
                continue

            if stripped.startswith("//"):
                continue

            cleaned_lines.append(line)

        fragment_source = "\n".join(cleaned_lines)

        if include_vertex:
            header = CustomShader._VERTEX_HEADER.strip("\n")
            fragment_source = fragment_source.replace(vertex_marker, header)

        vertex_file = pragma if pragma else "vertex.vert"
        vertex_source = game.paths.ShaderText(f"vertex/{vertex_file}")

        

        self._program = game._ctx.program(
            vertex_shader=vertex_source,
            fragment_shader=fragment_source
        )


    def __setattr__(self, name, value):
        if name == "_program":
            super().__setattr__(name, value)
        else:
            self._program[name] = value

    def __getattr__(self, name):
        return self._program[name].value
    



class TextRender:
    def __init__(self, game: GameType, custom_shader: CustomShader=None):
        self.game = game

        self.font_atlas = FontAtlas()

        self.ivbo = game._ctx.buffer(reserve=2048)

        self.program = custom_shader 

        self.vao = game._ctx.vertex_array(self.program._program, [(game._vbo, "2f 2f", "inPos", "inUV"), (self.ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=game._ebo)
        self.atlas_texture = load_texture(ctx=game._ctx, path=game.paths.AssetPath("atlas/fonts.png"))

        self.Position = glm.vec2(0)
        self.Scale = glm.vec2(25)
        self.SizeAtlas = glm.vec2(8)
        self.Zayer = 1

        self.StartX = 0
        self.StartY = 0
        self.SpaceX = 100
        self.SpaceY = 120
        self.NewLineX = 0

   

    def renderText(self, text: str):
        self.atlas_texture.use()

        self.ivbo.write(self.font_atlas.generateTextListByte(text, start_x=self.StartX, start_y=self.StartY, space_x=self.SpaceX, space_y=self.SpaceY, new_line_x=self.NewLineX))

        self.program._program["unPos"] = self.Position
        self.program._program["unScale"] = self.Scale
        self.program._program["unAtlas"] = self.SizeAtlas
        self.program._program["unZayer"] = self.Zayer
        self.program.GclTexture = 0


        self.vao.render(instances=self.font_atlas.instance_count)


class SpriteRender:
    def __init__(self):
        pass


    def renderSprite(self):
        pass

    
