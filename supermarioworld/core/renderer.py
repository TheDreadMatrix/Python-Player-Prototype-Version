from collections import defaultdict
from dataclasses import dataclass
from array import array

from supermarioworld.core.gl_utils import (
        moderngl, 
        create_error_texture, 
        _DEFAULT_FRAGMENT_SOURCE, 
        _DEFAULT_VERTEX_SOURCE
    )

import glm


RENDER_MODES = {
    0: moderngl.TRIANGLES,
    1: moderngl.LINE_LOOP,
    2: moderngl.LINE_STRIP,
    3: moderngl.POINTS,
    4: moderngl.TRIANGLE_FAN
}

class ShaderEntry:
    def __init__(self, game, custom_shader, default=False, vbo=None, ebo=None, vbo_only=None):
        self.program = custom_shader._program if not default else game._ctx.program(_DEFAULT_VERTEX_SOURCE, _DEFAULT_FRAGMENT_SOURCE)

        self.vao = game._ctx.vertex_array(self.program, [(vbo, "2f 2f", "inPos", "inCoord")], index_buffer=ebo)

        self.program["DM_Texture"] = 0

        self.uniforms = {
            "unPos": self.program["unPos"],
            "unSize": self.program["unSize"],
            "unLayer": self.program["unLayer"],
        
            "r": self.program["r"],
            "g": self.program["g"],
            "b": self.program["b"],
            "a": self.program["a"],

            "unFlx": self.program["unFlx"],
            "unFly": self.program["unFly"],
        }




@dataclass(slots=True)
class RenderPassCommand:
    texture: str
    size: tuple
    position: tuple
    
    r: float
    g: float
    b: float
    a: float


    layer: int
    flipx: bool
    flipy: bool
    shader: str





class MainRenderer:
    def __init__(self, game):
        self.game = game
        self.resources = game.assets

        self.layers = defaultdict(list)

        # Buffers
        vertices_only = array("f", [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        

        self.ebo = game._ctx.buffer(indices)
        self.vbo = game._ctx.buffer(vertices)
        self.vbo_only = game._ctx.buffer(vertices_only)

        self.projection = glm.ortho(0, game.width, game.height, 0, -1, 1)
        

        self.ubo = game._ctx.buffer(reserve=64)
        self.ubo.bind_to_uniform_block(0)
        self.ubo.write(self.projection.to_bytes())


        # Layers
        self.default_shader = ShaderEntry(game, 0, default=True, vbo=self.vbo, ebo=self.ebo, vbo_only=self.vbo_only)
        self.default_texture = create_error_texture(game._ctx)

        self.current_shader = self.default_shader

        # Cache
        self.last_texture_name = None
        self.last_shader_name = None

        

        
    
    def _eventResize(self):
        self.projection = glm.ortho(0, self.game.width, self.game.height, 0, -1, 1)
        self.ubo.write(self.projection.to_bytes())

        

    def clearPrompt(self):
        self.layers.clear()


    def submitMesh(self, size=(1, 1), position=(0, 0), r=1, g=1, b=1, a=1, layer=1, shader: str="default"):
        pass


    def submitSprite(self, texture: str, *, size=(1, 1), position=(0, 0), r=1, g=1, b=1, a=1, layer=1, flipx=False, flipy=False, shader: str="default"):
        self.layers[layer].append(
                RenderPassCommand(texture=texture, 
                                  size=size, 
                                  position=position, 
                                  r=r, 
                                  g=g, 
                                  b=b,
                                  a=a, 
                                  layer=layer, 
                                  flipx=flipx, 
                                  flipy=flipy, 
                                  shader=shader)
            )
        



    def renderSprite(self):
        all_layers = sorted(self.layers.keys())

        for layer in all_layers:

            commands = self.layers[layer]

            for cmd in commands:
                self._renderCommand(cmd)



    
    def render(self, texture_key, *, size=(1, 1), position=(0, 0), r=1, g=1, b=1, a=1, layer=1, flx=False, fly=False, shader_key="default", mode=0):
        if self.last_shader_name != shader_key:
            self.last_shader_name = shader_key
            self.current_shader = self.resources.shaders.get(shader_key, self.default_shader)
            
        shader = self.current_shader
        uniforms = shader.uniforms
        vao = shader.vao

        if self.last_texture_name != texture_key:
            self.last_texture_name = texture_key
            texture = self.resources.textures.get(texture_key, self.default_texture)
            texture.use(0)

        uniforms["unPos"].value = position
        uniforms["unSize"].value = size
        uniforms["unLayer"].value = layer
       
        uniforms["r"].value = r
        uniforms["g"].value = g
        uniforms["b"].value = b 
        uniforms["a"].value = a

        uniforms["unFlx"].value = flx
        uniforms["unFly"].value = fly
        
        vao.render(RENDER_MODES[mode])



        


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
       
        uniforms["r"].value = cmd.r
        uniforms["g"].value = cmd.g
        uniforms["b"].value = cmd.b 
        uniforms["a"].value = cmd.a

        uniforms["unFlx"].value = cmd.flipx
        uniforms["unFly"].value = cmd.flipy
        

        vao.render()

