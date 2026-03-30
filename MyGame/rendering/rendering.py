from MyGame.scenes_component import GameType
from MyGame.utilits.atlas import FontAtlas
from MyGame.requirements import glm, mgl, Image



def load_texture(game: GameType, path: str):
    img = Image.open(path).convert("RGBA")

    width, height = img.size
    img_data = img.tobytes()

    texture = game._ctx.texture((width, height), 4, img_data)
    texture.build_mipmaps()
    texture.filter = (mgl.NEAREST, mgl.NEAREST)

    return texture


class CustomShader:
    _VERTEX_HEADER = """#version 330 core\nin vec2 GclUv;\nout vec4 GclColor;\nuniform sampler2D GclTexture;"""
    _VERTEX_TEXT_HEADER = ""
    _PROHIBITED = {"fragment.frag", "vertex.vert", "text.vert", "text.frag"}
    _INCLUDE_VERTEX_MAP = {
        "vertex": "vertex.vert",
        "vertex.vert": "vertex.vert",
        "text": "text.vert",
        "text.vert": "text.vert",
        "vertex_text": "text.vert",
        "vertex_text.vert": "text.vert",
    }
    def __init__(self, game: GameType, shader_filename: str):
        if shader_filename in self._PROHIBITED:
            raise FileExistsError("Can not import building file")
        source = game.paths.ShaderText(f"custom/{shader_filename}")

        include_vertex = False
        include_vertex_text = False
        vertex_file_from_include = None
        vertex_marker = "__VERTEX_HEADER__"
        vertex_text_marker = "__VERTEX_TEXT__"

        lines = source.splitlines()
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("#include"):
                parts = stripped.split(maxsplit=1)
                if len(parts) < 2:
                    raise ValueError("Include must specify a target name")
                include_name = parts[1].strip().strip('"')
                if include_name not in CustomShader._INCLUDE_VERTEX_MAP:
                    raise ValueError(f"Unknown include: {include_name}")

                vertex_file = CustomShader._INCLUDE_VERTEX_MAP[include_name]
                if vertex_file_from_include and vertex_file_from_include != vertex_file:
                    raise ValueError("Conflicting vertex includes in one shader")
                vertex_file_from_include = vertex_file

                if include_name in ("vertex", "vertex.vert"):
                    include_vertex = True
                    cleaned_lines.append(vertex_marker)
                elif include_name in ("vertex_text", "vertex_text.vert"):
                    include_vertex_text = True
                    cleaned_lines.append(vertex_text_marker)
                else:
                    cleaned_lines.append("")
                continue

            if stripped.startswith("//"):
                continue

            cleaned_lines.append(line)

        fragment_source = "\n".join(cleaned_lines)

        if include_vertex:
            header = CustomShader._VERTEX_HEADER.strip("\n")
            fragment_source = fragment_source.replace(vertex_marker, header)
        if include_vertex_text:
            fragment_source = fragment_source.replace(vertex_text_marker, CustomShader._VERTEX_TEXT_HEADER)

        vertex_file = vertex_file_from_include or "vertex.vert"
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
    def __init__(self, game: GameType, custom_shader: CustomShader|None=None):
        self.game = game

        self.font_atlas = FontAtlas()

        self.ivbo = game._ctx.buffer(reserve=2048)

        self.program = custom_shader._program if custom_shader else game._ctx.program(game.paths.ShaderText("vertex/text.vert"), game.paths.ShaderText("fragment/text.frag")) 

        self.vao = game._ctx.vertex_array(self.program, [(game._vbo, "2f 2f", "inPos", "inUV"), (self.ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=game._ebo)
        self.atlas_texture = load_texture(game=game, path=game.paths.AssetPath("atlas/fonts.png"))

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

        self.program["unPos"] = self.Position
        self.program["unScale"] = self.Scale
        self.program["unAtlas"] = self.SizeAtlas
        self.program["unZayer"] = self.Zayer
        self.program["GclTexture"] = 0


        self.vao.render(instances=self.font_atlas.instance_count)


class SpriteRender:
    def __init__(self, game: GameType, custom_shader: CustomShader|None=None):
        self.game = game

        self.program = custom_shader._program if custom_shader else game._ctx.program(game.paths.ShaderText("vertex/vertex.vert"), game.paths.ShaderText("fragment/fragment.frag"))
        self.vao = game._ctx.vertex_array(self.program, [(game._vbo, "2f 2f", "inPos", "inUV")], index_buffer=game._ebo)
        

        self.Texture = None
        self.Position = glm.vec2(0)
        self.Scale = glm.vec2(100)
        self.Zayer = 1


    def renderSprite(self):
        if self.Texture:
            self.Texture.use()

        self.program["unPos"] = self.Position
        self.program["unScale"] = self.Scale
        self.program["unZayer"] = self.Zayer
        self.program["GclTexture"] = 0
        self.vao.render()

    
