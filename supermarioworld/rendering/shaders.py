from supermarioworld.core.gl_utils import _DEFAULT_VERTEX_SOURCE

class CustomShader:
    def __init__(self, game, shader_path: str):
        VERTEX_REPLACER = """#version 330 core

            in vec2 DM_Coord;
            out vec4 OutColor;
            uniform sampler2D DM_Texture;
            uniform vec3 rgb;
            uniform float alpha;
            """

        fragment_source = game.paths.ShaderText(shader_path)
        fragment_source = fragment_source.replace("#include vertex", VERTEX_REPLACER)
        
        self._program = game._ctx.program(
            _DEFAULT_VERTEX_SOURCE, 
            fragment_source
        )


    def setUniform(self, name, value) -> None:
        self._program[name] = value

    def getUniform(self, name):
        return self._program[name].value
