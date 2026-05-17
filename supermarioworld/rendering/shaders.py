

class CustomShader:
    _DEFAULT_VERTEX_SOURCE = """
        #version 330 core
        in vec2 inPos;
        in vec2 inCoord;

        layout(std140) uniform Projection{
            mat4 unProj;
        };

        uniform vec2 unPos;
        uniform vec2 unSize;
        uniform int unLayer;

        uniform bool unFlx;
        uniform bool unFly;

        out vec2 DM_Coord;

        void main(){
            vec2 finalPos = inPos * unSize + unPos;
            float finalLayer = float(unLayer) * 0.01;
            gl_Position = unProj * vec4(finalPos, finalLayer, 1.0);
            
            vec2 finalCoord = inCoord;

            if (unFlx) {
                finalCoord.x = 1.0 - finalCoord.x;
            }

            if (unFly) {
                finalCoord.y = 1.0 - finalCoord.y;
            }

            DM_Coord = finalCoord;
        }
    """


    _DEFAULT_FRAGMENT_SOURCE = """
        #version 330 core

        in vec2 DM_Coord;
        out vec4 OutColor;

        uniform sampler2D DM_Texture;
        uniform vec3 rgb;
        uniform float alpha;

        void main(){
            OutColor = texture(DM_Texture, DM_Coord) * vec4(rgb, alpha);
        }
    """


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
            self._DEFAULT_VERTEX_SOURCE, 
            fragment_source
        )


    def setUniform(self, name, value) -> None:
        self._program[name] = value

    def getUniform(self, name):
        return self._program[name].value
