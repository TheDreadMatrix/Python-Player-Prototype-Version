from supermarioworld.rendering._moderngl import load_texture
from supermarioworld.rendering.shaders import CustomShader
from collections import defaultdict
from dataclasses import dataclass







    
    



@dataclass(slots=True)
class RenderPassCommand:
    texture: str
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
        self.textures = {}


    def clearPrompt(self):
        self.layers.clear()


    def pushShader(self, key: str, shader: CustomShader):
        self.shaders.update({key: ShaderEntry(self._game, shader)})


    def pushTexture(self, key: str, path: str, filter: int=0, anisotropy: int=0):
        self.textures.update({key: load_texture(self._game._ctx, path, filter, anisotropy)})

    

    def _pushStraightTexture(self, key: str, texture):
        self.textures.update({key: texture})


    def submitSprite(self, 
               texture: str,
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
        all_layers = sorted(self.layers.keys())

        for layer in all_layers:

            commands = self.layers[layer]

            for cmd in commands:
                self._renderCommand(cmd)



        


    def _renderCommand(self, cmd: RenderPassCommand):
        shader = self.shaders[cmd.shader]
        program = shader.program
        vao = shader.vao

        texture = self.textures[cmd.texture]
        texture.use(0)

        program["DM_Texture"] = 0
        program["unPos"] = cmd.position
        program["unSize"] = cmd.size
        program["unLayer"] = cmd.layer
        program["alpha"] = cmd.alpha
        program["rgb"] = cmd.rgb
        program["unFlx"] = cmd.flipx
        program["unFly"] = cmd.flipy
        

        vao.render()

