from supermarioworld.typing.gametype import GameType
import re

from enum import Enum, auto
from dataclasses import dataclass

@dataclass(slots=True)
class ProcessResult:
    source: str
    include: str | None

class ShaderType(Enum):
    VERTEX = auto()
    FRAGMENT = auto()

class Include:
    def __init__(self, code: str, shader_type: ShaderType):
        self.code = code
        self.shader_type = shader_type



class DefaultUniform:
    def __init__(self, value):
        self.value = value


def _uniform(program, name, default):
    try:
        return program[name]
    except KeyError:
        return DefaultUniform(default)


def _strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)

    source = re.sub(r"//.*?$", "", source, flags=re.M)

    return source




# fix problem with shader input system or syntex error
# add own input attr
class _IncludeProcessor:
    def __init__(self):
        self.includes = {}
        self.include_count_for_source = 0

        DEFAULT_FRAGMENT_REPLACER = """
        #version 330 core
        in vec2 gluminary_Coordinate;
        out vec4 gluminary_FragColor;

        uniform sampler2D gluminary_Texture;

        uniform float gluminary_r;
        uniform float gluminary_g;
        uniform float gluminary_b;
        uniform float gluminary_a;

        
        vec4 getColorFromTexture(){
            return texture(gluminary_Texture, gluminary_Coordinate) * vec4(gluminary_r, gluminary_g, gluminary_b, gluminary_a);
        }
        """

        DEFAULT_VERTEX_REPLACER = """
        #version 330 core
        in vec2 gluminary_input_Position;
        in vec2 gluminary_input_Coordinate;

        layout(std140) uniform Projection{
            mat4 gluminary_Projection;
        };

        uniform vec2 gluminary_Position;
        uniform vec2 gluminary_Size;

        uniform bool gluminary_Flx;
        uniform bool gluminary_Fly;

        out vec2 gluminary_Coordinate;
        


        vec4 getPosition(){
            vec2 pre_position = gluminary_input_Position * gluminary_Size + gluminary_Position;
            
            vec4 final_position = gluminary_Projection * vec4(pre_position, 0, 1);
            return final_position;
        }

        void gotoFragment(){
            vec2 finalCoord = gluminary_input_Coordinate;

            if (gluminary_Flx) {
                finalCoord.x = 1.0 - finalCoord.x;
            }

            if (gluminary_Fly) {
                finalCoord.y = 1.0 - finalCoord.y;
            }

            gluminary_Coordinate = finalCoord;
        }

        """

        INSTANCE_VERTEX_REPLACER = """
                #version 330 core

                in vec2 gluminary_input_Position;
                in vec2 gluminary_input_Coordinate;


                in vec2 gluminary_instance_Position;
                in vec2 gluminary_instance_Size;

                in float gluminary_instance_Flx;
                in float gluminary_instance_Fly;



                layout(std140) uniform Projection {
                    mat4 gluminary_Projection;
                };


                uniform vec2 gluminary_Position;

                out vec2 gluminary_Coordinate;

                vec4 getPosition(){
                    vec2 pre_position = gluminary_input_Position * gluminary_instance_Size + gluminary_instance_Position + gluminary_Position;
                            
                    vec4 final_position = gluminary_Projection * vec4(pre_position, 0, 1);
                    return final_position;
                }

                void gotoFragment(){
                    vec2 finalCoord = gluminary_input_Coordinate;

                    if (gluminary_instance_Flx > 0) {
                        finalCoord.x = 1.0 - finalCoord.x;
                    }

                    if (gluminary_instance_Fly > 0) {
                        finalCoord.y = 1.0 - finalCoord.y;
                    }

                    gluminary_Coordinate = finalCoord;
                }

        """


        self.register("custom_instance_vertex", INSTANCE_VERTEX_REPLACER, ShaderType.VERTEX)
        self.register("custom_default_vertex", DEFAULT_VERTEX_REPLACER, ShaderType.VERTEX)

        self.register("custom_fragment", DEFAULT_FRAGMENT_REPLACER, ShaderType.FRAGMENT)

       

    def register(self, name: str, source: str, shader_type: ShaderType):
        self.includes[name] = Include(source, shader_type)

    

    def process(self, source: str, which_type):
        self.include_count_for_source = 0

        clean_source = _strip_comments(source)

        clean_lines = clean_source.splitlines()
        real_lines = source.splitlines()

        out = []

        for real_line, clean_line in zip(real_lines, clean_lines):
            stripped = clean_line.strip()

            if stripped.startswith("#include"):
                self.include_count_for_source += 1

                if self.include_count_for_source > 1:
                    raise SyntaxError(
                        "Only one #include is allowed per shader."
                    )

                parts = stripped.split()

                if len(parts) != 2:
                    raise SyntaxError(f"Invalid include: {real_line}")

                include_name = parts[1]

                if include_name not in self.includes:
                    raise SyntaxError(
                        f"Unknown include '{include_name}'"
                    )

                include = self.includes[include_name]

                if include.shader_type != which_type:
                    raise SyntaxError(
                        f"Include '{include_name}' is for "
                        f"{include.shader_type.name.lower()} shader, "
                        f"but used in {which_type.name.lower()} shader."
                    )

                out.append(include.code)
                used_include = include_name

            else:
                out.append(real_line)

        return ProcessResult(source="\n".join(out), include=used_include)


_processor = _IncludeProcessor()



class CustomShader:
    def __init__(self, game: GameType, vertex_path: str, fragment_path: str):
        renderer = game.renderer


        # load sources
        vertex_source = game.paths.ShaderText(vertex_path)
        fragment_source = game.paths.ShaderText(fragment_path)

        # preprocess includes (BOTH)
        vertex = _processor.process(vertex_source, which_type=ShaderType.VERTEX)
        fragment = _processor.process(fragment_source, which_type=ShaderType.FRAGMENT)

        

        # compile program
        self._program = renderer._ctx.program(vertex_shader=vertex.source, fragment_shader=fragment.source)
        


        # uniform and vao registry
        self._uniforms = {}
        
        self._uniforms.update({
            "unPos": _uniform(self._program, "gluminary_Position", (1, 1)),
            "unSize": _uniform(self._program, "gluminary_Size", (1, 1)),

            "unFlx": _uniform(self._program, "gluminary_Flx", 0),
            "unFly": _uniform(self._program, "gluminary_Fly", 0),

            "r": _uniform(self._program, "gluminary_r", 1.0),
            "g": _uniform(self._program, "gluminary_g", 1.0),
            "b": _uniform(self._program, "gluminary_b", 1.0),
            "a": _uniform(self._program, "gluminary_a", 1.0),
        })

        
        self._vao = renderer._ctx.vertex_array(self._program, 
            [(renderer.vbo, "2f 2f", "gluminary_input_Position", "gluminary_input_Coordinate")], index_buffer=renderer.ebo)
        

        # self._uniforms = {}
        # self._vao = game.renderer._ctx.vertex_array(self._program, [(game.renderer.vbo)])
        
        

    def setUniform(self, name: str, value):
        self._program[name] = value


    def getUniform(self, name):
        return self._program[name].value
        

    def __repr__(self):
        return "<CustomShader - GLuminary>"