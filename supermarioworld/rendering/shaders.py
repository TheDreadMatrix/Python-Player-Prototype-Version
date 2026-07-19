from supermarioworld.typing.gametype import GameType
from supermarioworld.core.gl_utils.gl_sources import INSTANCE_VERTEX_REPLACER, DEFAULT_VERTEX_REPLACER, DEFAULT_FRAGMENT_REPLACER

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




# add own input attr
class _IncludeProcessor:
    def __init__(self):
        self.includes = {}
        self.include_count_for_source = 0

        


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
        
        
        
    def setUniform(self, name: str, value):
        self._program[name] = value


    def getUniform(self, name):
        return self._program[name].value
        

    def __repr__(self):
        return "<CustomShader - GLuminary>"