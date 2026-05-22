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





class MainRenderer:
    def __init__(self, game):
        self.game = game
        self.resources = game.assets

        self.layers = defaultdict(list)

        # Layers
        self.default_shader = game.assets.default_shader
        self.default_texture = game.assets.default_texture

        self.current_shader = self.default_shader

        # Cache
        self.last_texture_name = None
        self.last_shader_name = None
        
        

    def clearPrompt(self):
        self.layers.clear()


    def submitMesh(self, size=(1, 1), position=(0, 0), rgb=(1, 1, 1), alpha=1, layer=1, shader: str="default"):
        pass


    def submitSprite(self, texture: str, *, size=(1, 1), position=(0, 0), rgb=(1, 1, 1), alpha=1, layer=1, flipx=False, flipy=False, shader: str="default"):
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
        if self.last_shader_name != cmd.shader:
            self.last_shader_name = cmd.shader
            self.current_shader = self.resources.shaders.get(cmd.shader, self.default_shader)
            
        shader = self.current_shader
        uniforms = shader.uniforms
        vao = shader.vao

        if self.last_texture_name != cmd.texture:
            self.last_texture_name = cmd.texture
            texture = self.resources.textures.get(cmd.texture, self.default_texture)
            texture.use(0)
            

        uniforms["unPos"].value = cmd.position
        uniforms["unSize"].value = cmd.size
        uniforms["unLayer"].value = cmd.layer
        uniforms["alpha"].value = cmd.alpha
        uniforms["rgb"].value = cmd.rgb
        uniforms["unFlx"].value = cmd.flipx
        uniforms["unFly"].value = cmd.flipy
        

        vao.render()

