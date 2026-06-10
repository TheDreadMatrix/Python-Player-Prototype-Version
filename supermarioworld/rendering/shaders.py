from supermarioworld.package_typing import GameType

"""
Gluminary Contract GLSL extension building with Daemon Engine

#include custom_default
#include custom_instance
#include custom_quad

* If we including second or more time. Raise SyntaxError. Use only one include custom for vertex and fragment shader
* You set custom uniform by setUniform. But you can define uniforms one time in __init__ and use setUniformByOneTime
* Also after including and create CustomShader there generate glsl source with mergining

Also VAO must create attribute for each shader

Default -> [gluminary_input_Position, gluminary_input_Coordinate]
Quad -> [gluminary_input_Position]
Instance -> [gluminary_input_Position, gluminary_input_Coordinate, gluminary_instance_Position, gluminary_instance_Size, gluminary_instance_Flx, gluminary_instance_Fly]

For uniforms shader builds building uniform attribute for each shader

Default -> [uniform vec2 gluminary_Position; uniform vec2 gluminary_Size; uniform bool gluminary_Flx; uniform bool gluminary_Fly;]
Quad -> [uniform vec2 gluminary_Position; uniform vec2 gluminary_Size]
Instance -> [uniform vec2 gluminary_Position;]

Also for fragment uniforms:

[gluminary_r, gluminary_g, gluminary_b, gluminary_a] for all shader type

[gluminary_Texture] for Default and Instance shaders


"""


# The problem if we including 2 times other shaders we dont recieve error but code cannot compiling with error 
class _IncludeProcessor:
    def __init__(self):
        self.includes = {}
        self.used = set()

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

        void giveFragmentUvCoordinate(){
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

        self.register("custom_default_vertex", DEFAULT_VERTEX_REPLACER)
        self.register("custom_fragment_texture", DEFAULT_FRAGMENT_REPLACER)

        self.register("custom_quad", "Hello")
        self.register("custom_instance", "hello")

    def register(self, name: str, code: str):
        self.includes[name] = code

    def process(self, source: str):
        self.used.clear()

        while "#include" in source:
            lines = source.split("\n")
            out = []

            for line in lines:
                line_stripped = line.strip()

                if line_stripped.startswith("#include"):
                    parts = line_stripped.split()
                    if len(parts) != 2:
                        raise SyntaxError(f"Invalid include syntax: {line}")

                    name = parts[1]

                    if name in self.used:
                        raise SyntaxError(f"Duplicate include: {name}")

                    if name not in self.includes:
                        raise SyntaxError(f"Unknown include: {name}")

                    self.used.add(name)
                    out.append(self.includes[name])

                else:
                    out.append(line)

            source = "\n".join(out)

        return source





class CustomShader:
    def __init__(self, game: GameType, vertex_path: str, fragment_path: str):
        self.processor = _IncludeProcessor()


        # load sources
        vertex_source = game.paths.ShaderText(vertex_path)
        fragment_source = game.paths.ShaderText(fragment_path)

        # preprocess includes (BOTH)
        vertex_source = self.processor.process(vertex_source)
        fragment_source = self.processor.process(fragment_source)

        # compile program
        self._program = game.renderer._ctx.program(
            vertex_shader=vertex_source,
            fragment_shader=fragment_source
        )

        # uniform registry
        self._uniforms = {
            "unPos": self._program["gluminary_Position"],
            "unSize": self._program["gluminary_Size"],
            "unFlx": self._program["gluminary_Flx"],
            "unFly": self._program["gluminary_Fly"],
            "r": self._program["gluminary_r"],
            "g": self._program["gluminary_g"],
            "b": self._program["gluminary_b"],
            "a": self._program["gluminary_a"]
            
        }

        self._vao = game.renderer._ctx.vertex_array(self._program, [(game.renderer.vbo, "2f 2f", "gluminary_input_Position", "gluminary_input_Coordinate")], index_buffer=game.renderer.ebo)
        






    def setUniform(self, name: str, value):
        self._program[name] = value


    def defineUniform(self, alias: str, uniform_name: str):
        self._uniforms[alias] = self._program[uniform_name]

    def setUniformByOneTime(self, key: str, value):
        self._uniforms[key].value = value

    def getUniform(self, name):
        return self._program[name].value
        