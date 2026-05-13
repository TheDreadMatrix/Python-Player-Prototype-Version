from supermarioworld.rendering.moderngl import moderngl

from collections import defaultdict
from dataclasses import dataclass



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




    
    



@dataclass
class RenderPassCommand:
    texture: moderngl.Texture
    size: tuple
    position: tuple
    rgb: tuple
    alpha: int
    layer: int
    flipx: bool
    flipy: bool
    shader: str


class ShaderEntry:
    def __init__(self, game, custom_shader: CustomShader, default=False):
         
        self.program = custom_shader._program if not default else game._ctx.program(CustomShader._DEFAULT_VERTEX_SOURCE, CustomShader._DEFAULT_FRAGMENT_SOURCE)
        self.vao = game._ctx.vertex_array(self.program, [(game._vbo, "2f 2f", "inPos", "inCoord")], index_buffer=game._ebo)




class MainRenderer:
    def __init__(self, game):
        self._game = game

        self.layers = defaultdict(list)
        self.shaders = {"default": ShaderEntry(game, 0, True)}


    def clearPrompt(self):
        self.layers.clear()


    def pushShader(self, key, shader: CustomShader):
        self.shaders.update({key: ShaderEntry(self._game, shader)})


    def submitSprite(self, 
               texture: moderngl.Texture,
               *,
               size=(1, 1), 
               position=(0, 0), 
               rgb=(1, 1, 1),
               alpha=1,
               layer=1,
               flipx=False,
               flipy=False,
               shader: str="default"
               ):
        
        self.layers[layer].append(
                RenderPassCommand(texture=texture, size=size, position=position, rgb=rgb, alpha=alpha, layer=layer, flipx=flipx, flipy=flipy, shader=shader)
            )
        



    def renderSprite(self):
        ctx = self._game._ctx

        ctx.enable(moderngl.DEPTH_TEST)
        ctx.enable(moderngl.BLEND)

        ctx.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA
        )


        ctx.depth_mask = True

        for layer in sorted(self.layers.keys()):

            commands = self.layers[layer]

            for cmd in commands:

                if cmd.alpha < 1.0:
                    continue

                self._renderCommand(cmd)


        ctx.depth_mask = False

        for layer in sorted(self.layers.keys()):

            commands = self.layers[layer]

            transparent = []

            for cmd in commands:

                if cmd.alpha < 1.0:
                    transparent.append(cmd)

    

            for cmd in transparent:
                self._renderCommand(cmd)


        ctx.depth_mask = True





    def _renderCommand(self, cmd: RenderPassCommand):
        shader = self.shaders[cmd.shader]
        program = shader.program
        vao = shader.vao

        cmd.texture.use(0)

        program["DM_Texture"] = 0
        program["unPos"] = cmd.position
        program["unSize"] = cmd.size
        program["unLayer"] = cmd.layer
        program["alpha"] = cmd.alpha
        program["rgb"] = cmd.rgb
        program["unFlx"] = cmd.flipx
        program["unFly"] = cmd.flipy
        

        vao.render()

