from supermarioworld.typing.gametype import GameType
import re


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
# fix for instance shader
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

        self.register("custom_instance_vertex", "hello")
        self.register("custom_default_vertex", DEFAULT_VERTEX_REPLACER)

        self.register("custom_fragment", DEFAULT_FRAGMENT_REPLACER)

       

    def register(self, name: str, code: str):
        self.includes[name] = code

    

    def process(self, source: str):
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

                include = parts[1]

                if include not in self.includes:
                    raise SyntaxError(
                        f"Unknown include '{include}'"
                    )

                out.append(self.includes[include])

            else:
                out.append(real_line)

        return "\n".join(out)


_processor = _IncludeProcessor()



class CustomShader:
    def __init__(self, game: GameType, vertex_path: str, fragment_path: str):
        


        # load sources
        vertex_source = game.paths.ShaderText(vertex_path)
        fragment_source = game.paths.ShaderText(fragment_path)

        # preprocess includes (BOTH)
        vertex_source = _processor.process(vertex_source)
        fragment_source = _processor.process(fragment_source)

        

        # compile program
        self._program = game.renderer._ctx.program(vertex_shader=vertex_source, fragment_shader=fragment_source)
        
      


        # uniform registry
        self._uniforms = {
            "unPos": _uniform(self._program, "gluminary_Position", (1, 1)),
            "unSize": _uniform(self._program, "gluminary_Size", (1, 1)),

            "unFlx": _uniform(self._program, "gluminary_Flx", 0),
            "unFly": _uniform(self._program, "gluminary_Fly", 0),

            "r": _uniform(self._program, "gluminary_r", 1.0),
            "g": _uniform(self._program, "gluminary_g", 1.0),
            "b": _uniform(self._program, "gluminary_b", 1.0),
            "a": _uniform(self._program, "gluminary_a", 1.0),
        }

        
        self._vao = game.renderer._ctx.vertex_array(self._program, 
            [(game.renderer.vbo, "2f 2f", "gluminary_input_Position", "gluminary_input_Coordinate")], index_buffer=game.renderer.ebo)
        
        

    def setUniform(self, name: str, value):
        self._program[name] = value


    def getUniform(self, name):
        return self._program[name].value
        