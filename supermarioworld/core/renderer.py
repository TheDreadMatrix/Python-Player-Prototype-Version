from array import array

from supermarioworld.core.gl_utils.gl_textures import moderngl, create_error_texture
from supermarioworld.core.gl_utils.gl_sources import (
    _DEFAULT_VERTEX_SOURCE_INSTANCE,
    _DEFAULT_FRAGMENT_SOURCE, 
    _DEFAULT_FRAGMENT_SOURCE_MESH, 
    _DEFAULT_VERTEX_SOURCE, 
    _DEFAULT_VERTEX_SOURCE_MESH
)

import numpy
import glm


RENDER_MODES = {
    0: moderngl.TRIANGLES,
    1: moderngl.LINE_LOOP,
    2: moderngl.LINE_STRIP,
    3: moderngl.POINTS,
    4: moderngl.TRIANGLE_FAN
}


class RenderTarget:
    def __init__(self, ctx: moderngl.Context, size):
        self.texture = ctx.texture(size, 4)
        
        self.fbo = ctx.framebuffer(
            color_attachments=[self.texture]
        )

    def use(self):
        self.fbo.use()

    def clear(self):
        self.fbo.clear(0, 0, 0, 0)

    def delete(self):
        self.fbo.release()
        self.texture.release()
        


class ShaderEntry:
    def __init__(self, ctx: moderngl.Context, custom_shader, shader_type=0, vbo=None, ebo=None, vbo_instance=None):
        self.ctx = ctx
        self.shader_type = shader_type

        if shader_type == 0:
            self.program = ctx.program(_DEFAULT_VERTEX_SOURCE, _DEFAULT_FRAGMENT_SOURCE)
            self.program["DM_Texture"] = 0

        elif shader_type == 1:
            self.program = ctx.program(_DEFAULT_VERTEX_SOURCE_MESH, _DEFAULT_FRAGMENT_SOURCE_MESH)

        elif shader_type == 2:
            self.program = ctx.program(_DEFAULT_VERTEX_SOURCE_INSTANCE, _DEFAULT_FRAGMENT_SOURCE)
            self.program["DM_Texture"] = 0

        else:
            self.program = custom_shader._program
            

        self._buildVao(vbo, ebo, vbo_instance, custom_shader)
        self._buildUniforms(custom_shader)


    def _buildVao(self, vbo, ebo, vbo_instance, custom_shader):
        if self.shader_type == 0:
            self.vao = self.ctx.vertex_array(self.program, [(vbo, "2f 2f", "inPos", "inCoord")], index_buffer=ebo)
        elif self.shader_type == 1:
            self.vao = self.ctx.vertex_array(self.program, [(vbo, "2f", "inPos")], index_buffer=ebo)
        elif self.shader_type == 2:
            self.vao = self.ctx.vertex_array(self.program, [(vbo, "2f 2f", "inPos", "inCoord"), 
                                                            (vbo_instance, "2f 2f 1f 1f/i", "instancePos", "instanceSize", "instanceFlx", "instanceFly")], index_buffer=ebo)
        else:
            self.vao = custom_shader._vao

    def _buildUniforms(self, custom_shader):
        if self.shader_type == 0:
            self.uniforms = self.uniforms = {
                "unPos": self.program["unPos"],
                "unSize": self.program["unSize"],
            
                "r": self.program["r"],
                "g": self.program["g"],
                "b": self.program["b"],
                "a": self.program["a"],

                "unFlx": self.program["unFlx"],
                "unFly": self.program["unFly"],
            }
        elif self.shader_type == 1:
            self.uniforms = {
                "unPos": self.program["unPos"],
                "unSize": self.program["unSize"],
                "r": self.program["r"],
                "g": self.program["g"],
                "b": self.program["b"],
                "a": self.program["a"],
            }
        elif self.shader_type == 2:
            self.uniforms = {
                "r": self.program["r"],
                "g": self.program["g"],
                "b": self.program["b"],
                "a": self.program["a"]
            }
        else:
            self.uniforms = custom_shader._uniforms



class MainRenderer:
    def __init__(self, game):
        self.game = game
        self.resources = game.assets

        self.shaders: dict[str, ShaderEntry] = {}
        self.fbos: dict[str, RenderTarget] = {}


        # Buffers
        vertices_only = array("f", [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        # Create render context
        self._ctx = moderngl.create_context()
        self._ctx.enable(moderngl.BLEND)
        self._ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        self._ctx.viewport = (0, 0, game.width, game.height)
        self._ctx.point_size = 10.0
        self._ctx.line_width = 5.0

        

        self.ebo = self._ctx.buffer(indices)
        self.vbo = self._ctx.buffer(vertices)
        self.vbo_only = self._ctx.buffer(vertices_only)
        self.vbo_instance = self._ctx.buffer(reserve=1024 * 1024)

        self.projection = glm.ortho(0, game.width, game.height, 0, -1, 1)
        

        self.ubo = self._ctx.buffer(reserve=64)
        self.ubo.bind_to_uniform_block(0)
        self.ubo.write(self.projection.to_bytes())


        # Layers
        self.default_shader = ShaderEntry(self._ctx, 0, shader_type=0, vbo=self.vbo, ebo=self.ebo, vbo_instance=self.vbo_instance)
        self.default_shader_mesh = ShaderEntry(self._ctx, 0, shader_type=1, vbo=self.vbo_only, ebo=self.ebo, vbo_instance=None)
        self.default_shader_instance = ShaderEntry(self._ctx, 0, shader_type=2, vbo=self.vbo, ebo=self.ebo, vbo_instance=self.vbo_instance)

        self.default_texture = create_error_texture(self._ctx)

        self.current_shader = self.default_shader
        self.current_fbo = None

        # Cache
        self.last_texture_name = None
        self.last_shader_name = None

        

        
    
    def _eventResize(self):
        self.projection = glm.ortho(0, self.game.width, self.game.height, 0, -1, 1)
        self.ubo.write(self.projection.to_bytes())


    def _clearColor(self, r, g, b):
        self._ctx.clear(r, g, b, 1)

    def _renderTexture(self, texture, *, size=(1,1), position=(0,0),
                   r=1, g=1, b=1, a=1,
                   flx=False, fly=False,
                   shader_key="default", mode=0):

        if self.last_shader_name != shader_key:
            self.last_shader_name = shader_key
            self.current_shader = self.shaders.get(
                shader_key,
                self.default_shader
            )

        shader = self.current_shader
        uniforms = shader.uniforms
        vao = shader.vao

        texture.use(0)

        uniforms["unPos"].value = position
        uniforms["unSize"].value = size

        uniforms["r"].value = r
        uniforms["g"].value = g
        uniforms["b"].value = b
        uniforms["a"].value = a

        uniforms["unFlx"].value = flx
        uniforms["unFly"].value = fly

        vao.render(RENDER_MODES[mode])


    def regShader(self, shader_key, your_shader):
        self.shaders.update({shader_key: ShaderEntry(self._ctx, your_shader, shader_type=-1)})


    def delShader(self, shader_key):
        shader = self.shaders.pop(shader_key, None)
        if shader is not None:
            shader.uniforms.clear()
            shader.program.release()
            shader.vao.release()


    def createFbo(self, frame_key, size):
        self.fbos.update({frame_key: RenderTarget(self._ctx, size)})

    def deleteFbo(self, frame_key):
        fbo = self.fbos.pop(frame_key, None)
        fbo.delete()

    def beginFbo(self, frame_key):
        if frame_key not in self.fbos:
            return
        
        self.current_fbo = self.fbos[frame_key]
        self.current_fbo.use()
        self.current_fbo.clear()

    def endFbo(self):
        self._ctx.screen.use()
        

    def renderFbo(self, frame_key, *, position=(0, 0), size=(1, 1), r=1, g=1, b=1, a=1, flx=False, fly=True, shader_key="default", mode=0):
        tex = self.fbos[frame_key].texture if frame_key in self.fbos else self.default_texture
        self._renderTexture(tex, position=position, size=size, r=r, g=g, b=b, a=a, flx=flx, fly=fly, shader_key=shader_key, mode=mode)
        


    def renderQuad(self, position=(0, 0), size=(100, 100), r=1, g=1, b=1, a=1, mode=0):
        shader = self.default_shader_mesh

        uniforms = shader.uniforms

        uniforms["unPos"].value = position
        uniforms["unSize"].value = size
        uniforms["r"].value = r
        uniforms["g"].value = g
        uniforms["b"].value = b 
        uniforms["a"].value = a

        shader.vao.render(RENDER_MODES[mode])
        


    # 2f 2f i i / i
    # position size flx fly
    def renderInstance(self, texture_key, *, r=1, g=1, b=1, a=1, shader_key="instance", mode=0, instances=[]):
        if self.last_shader_name != shader_key:
            self.last_shader_name = shader_key

            self.current_shader = (
                self.shaders.get(
                    shader_key,
                    self.default_shader_instance
                )
                )

        shader = self.current_shader


        if self.last_texture_name != texture_key:
            self.last_texture_name = texture_key

            texture = (self.resources.textures.get(texture_key, self.default_texture))

            texture.use(0)

    

        data = numpy.array(instances, dtype="f4").flatten()

        self.vbo_instance.orphan()

        self.vbo_instance.write(data)

        shader.uniforms["r"].value = r
        shader.uniforms["g"].value = g
        shader.uniforms["b"].value = b
        shader.uniforms["a"].value = a

        shader.vao.render(
            RENDER_MODES[mode],
            instances=len(instances)
        )


    
    def render(self, texture_key, *, size=(1, 1), position=(0, 0), r=1, g=1, b=1, a=1, flx=False, fly=False, shader_key="default", mode=0):
        if self.last_shader_name != shader_key:
            self.last_shader_name = shader_key
            self.current_shader = self.shaders.get(shader_key, self.default_shader)
            
        shader = self.current_shader
        uniforms = shader.uniforms
        vao = shader.vao

        if self.last_texture_name != texture_key:
            self.last_texture_name = texture_key
            texture = self.resources.textures.get(texture_key, self.default_texture)
            texture.use(0)

        uniforms["unPos"].value = position
        uniforms["unSize"].value = size
       
        uniforms["r"].value = r
        uniforms["g"].value = g
        uniforms["b"].value = b 
        uniforms["a"].value = a

        uniforms["unFlx"].value = flx
        uniforms["unFly"].value = fly
        
        vao.render(RENDER_MODES[mode])





