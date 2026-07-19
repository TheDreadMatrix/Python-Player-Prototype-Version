from supermarioworld.core.gl_utils.gl_textures import moderngl, create_error_texture
from supermarioworld.core.gl_utils.gl_sources import (
    _DEFAULT_VERTEX_SOURCE_INSTANCE,
    _DEFAULT_FRAGMENT_SOURCE, 
    _DEFAULT_FRAGMENT_SOURCE_MESH, 
    _DEFAULT_VERTEX_SOURCE, 
    _DEFAULT_VERTEX_SOURCE_MESH
)

import numpy as np
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
            self.program["gluminary_Texture"] = 0
            

        elif shader_type == 1:
            self.program = ctx.program(_DEFAULT_VERTEX_SOURCE_MESH, _DEFAULT_FRAGMENT_SOURCE_MESH)

        elif shader_type == 2:
            self.program = ctx.program(_DEFAULT_VERTEX_SOURCE_INSTANCE, _DEFAULT_FRAGMENT_SOURCE)
            self.program["gluminary_Texture"] = 0

        else:
            self.program = custom_shader._program
            

        self._buildVao(vbo, ebo, vbo_instance, custom_shader)
        self._buildUniforms(custom_shader)


    def _buildVao(self, vbo, ebo, vbo_instance, custom_shader):
        if self.shader_type == 0:
            self.vao = self.ctx.vertex_array(self.program, [(vbo, "2f 2f", "gluminary_input_Position", "gluminary_input_Coordinate")], index_buffer=ebo)
        elif self.shader_type == 1:
            self.vao = self.ctx.vertex_array(self.program, [(vbo, "2f", "inPos")], index_buffer=ebo)
        elif self.shader_type == 2:
            self.vao = self.ctx.vertex_array(self.program, [(vbo, "2f 2f", "gluminary_input_Position", "gluminary_input_Coordinate"), 
                                                            (vbo_instance, "2f 2f 1f 1f/i", 
                                                             "gluminary_instance_Position", 
                                                             "gluminary_instance_Size", 
                                                             "gluminary_instance_Flx", 
                                                             "gluminary_instance_Fly")], index_buffer=ebo)
        else:
            self.vao = custom_shader._vao

    def _buildUniforms(self, custom_shader):
        # Default shader
        if self.shader_type == 0:
            self.uniforms = {
                "unPos": self.program["gluminary_Position"],
                "unSize": self.program["gluminary_Size"],
            
                "r": self.program["gluminary_r"],
                "g": self.program["gluminary_g"],
                "b": self.program["gluminary_b"],
                "a": self.program["gluminary_a"],

                "unFlx": self.program["gluminary_Flx"],
                "unFly": self.program["gluminary_Fly"],
            }

        # Quad shader
        elif self.shader_type == 1:
            self.uniforms = {
                "unPos": self.program["unPos"],
                "unSize": self.program["unSize"],
                "r": self.program["r"],
                "g": self.program["g"],
                "b": self.program["b"],
                "a": self.program["a"],
            }

        # Instance
        elif self.shader_type == 2:
            self.uniforms = {
                "r": self.program["gluminary_r"],
                "g": self.program["gluminary_g"],
                "b": self.program["gluminary_b"],
                "a": self.program["gluminary_a"],
                "unPos": self.program["gluminary_Position"]
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
        vertices_only = np.array([0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        vertices = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

        # Create render context
        self._ctx = moderngl.create_context()
        self._ctx.enable(moderngl.BLEND)
        self._ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        self._ctx.viewport = (0, 0, game.width, game.height)
        self._ctx.point_size = 5.0
        self._ctx.line_width = 2.0

        

        self.ebo = self._ctx.buffer(indices)
        self.vbo = self._ctx.buffer(vertices)
        self.vbo_only = self._ctx.buffer(vertices_only)
        self.vbo_instance = self._ctx.buffer(reserve=1024 * 1024)

        self.projection = glm.ortho(0, game.width, game.height, 0, -1, 1)
        

        self.ubo = self._ctx.buffer(reserve=64)
        self.ubo.bind_to_uniform_block(0)
        self.ubo.write(self.projection.to_bytes())


        # Shaders
        self.default_shader = ShaderEntry(self._ctx, 0, shader_type=0, vbo=self.vbo, ebo=self.ebo, vbo_instance=self.vbo_instance)
        
        self.default_shader_mesh = ShaderEntry(self._ctx, 0, shader_type=1, vbo=self.vbo_only, ebo=self.ebo, vbo_instance=None)
        self.default_shader_instance = ShaderEntry(self._ctx, 0, shader_type=2, vbo=self.vbo, ebo=self.ebo, vbo_instance=self.vbo_instance)

        self.default_texture = create_error_texture(self._ctx)

        self.current_shader = self.default_shader
        self._fbo_stack = []

        # Res
        self._owner = None
        self.set_to_destroy = {}

        # Cache
        self.last_texture_name = ""
        self.last_shader_name = ""

        

        
    # Backend methods
    def _eventResize(self):
        self.projection = glm.ortho(0, self.game.width, self.game.height, 0, -1, 1)
        self.ubo.write(self.projection.to_bytes())


    def _clearColor(self, r, g, b):
        self._ctx.clear(r, g, b, 1)


    # GPU resources
    def beginScene(self, scene_name):
        self._owner = scene_name

    def _set_to_stack(self, owner, resource_type, resource_key):
        self.set_to_destroy.setdefault(owner, [])
        self.set_to_destroy[owner].append((resource_type, resource_key))

    def releaseScene(self):
        for typ, key in self.set_to_destroy.pop(self._owner, []):
            if typ == "shader":
                self.delShader(key)
            elif typ == "frame":
                self.deleteFbo(key)


    def regShader(self, shader_key, your_shader):
        self.shaders.update({shader_key: ShaderEntry(self._ctx, your_shader, shader_type=-1)})
        self._set_to_stack(self._owner, "shader", shader_key)


    def delShader(self, shader_key):
        shader = self.shaders.pop(shader_key, None)
        if shader is not None:
            shader.uniforms.clear()
            shader.program.release()
            shader.vao.release()


    def createFbo(self, frame_key, size):
        self.fbos.update({frame_key: RenderTarget(self._ctx, size)})
        self._set_to_stack(self._owner, "frame", frame_key)


    def deleteFbo(self, frame_key):
        fbo = self.fbos.pop(frame_key, None)
        fbo.delete()

    # Fbo methods
    def beginFbo(self, frame_key):
        fbo = self.fbos.get(frame_key)

        if not fbo:
            return

        self._fbo_stack.append(fbo)

        fbo.use()
        fbo.clear()

    def endFbo(self):
        if not self._fbo_stack:
            self._ctx.screen.use()
            return

        self._fbo_stack.pop()

        if self._fbo_stack:
            self._fbo_stack[-1].use()
        else:
            self._ctx.screen.use()


    # Rendering
    def _renderTexture(self, texture, *, size=(1,1), position=(0,0), r=1, g=1, b=1, a=1, flx=False, fly=False, shader_key="default"):

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

        vao.render()
        

    def renderFbo(self, frame_key, *, position=(0, 0), size=(1, 1), r=1, g=1, b=1, a=1, flx=False, fly=True, shader_key="default"):
        tex = self.fbos[frame_key].texture if frame_key in self.fbos else self.default_texture
        self._renderTexture(tex, position=position, size=size, r=r, g=g, b=b, a=a, flx=flx, fly=fly, shader_key=shader_key)
        


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
    def renderInstance(self, texture_key, *, position=(0, 0), r=1, g=1, b=1, a=1, shader_key="instance", instances=[]):
        if self.last_shader_name != shader_key:
            self.last_shader_name = shader_key
            self.current_shader = self.shaders.get(shader_key, self.default_shader_instance)

        shader = self.current_shader


        if self.last_texture_name != texture_key:
            self.last_texture_name = texture_key
            texture = (self.resources.textures.get(texture_key, self.default_texture))
            texture.use(0)

    

        data = np.array(instances, dtype="f4").flatten()

        self.vbo_instance.orphan()

        self.vbo_instance.write(data)

        shader.uniforms["r"].value = r
        shader.uniforms["g"].value = g
        shader.uniforms["b"].value = b
        shader.uniforms["a"].value = a
        shader.uniforms["unPos"].value = position

        shader.vao.render(instances=len(instances))

        


    
    def render(self, texture_key, *, size=(1, 1), position=(0, 0), r=1, g=1, b=1, a=1, flx=False, fly=False, shader_key="default"):
        texture = self.resources.textures.get(texture_key, self.default_texture)
        self._renderTexture(texture, position=position, size=size, r=r, g=g, b=b, a=a, flx=flx, fly=fly, shader_key=shader_key)






