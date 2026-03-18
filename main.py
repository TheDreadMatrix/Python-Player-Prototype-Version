import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from MyGame import SceneManager, johnson
import pygame as pg
import moderngl as mgl
import glm
from array import array


class Programs:
    def __init__(self, game: "MyGame"):
        class ShaderConstant:
            IN_POS="inPos"
            IN_UV="inUV"
            IN_TEXT_POS="inTextPos"
            IN_TEXT_OFFSET="inTextOffset"


        self.GLSL = ShaderConstant
        self.shader_textures = game.ctx.program(johnson.readShader("textures/shader.vert"), johnson.readShader("textures/shader.frag"))
        self.shader_text = game.ctx.program(johnson.readShader("text/shader.vert"), johnson.readShader("text/shader.frag"))
        self.shader_pp = game.ctx.program(johnson.readShader("post-proccessing/shader.vert"), johnson.readShader("post-proccessing/shader.frag"))


class MyGame:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self.window = pg.display.set_mode((800, 600), flags=pg.DOUBLEBUF|pg.OPENGL|pg.RESIZABLE)
        pg.display.set_caption("Super Mario World: 91P Retitle")
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.BLEND)
        self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self.ctx.viewport = (0, 0, *self.window.get_size())

        self.clock = pg.time.Clock()

        self.delta_time = 0
        self.time_fbo_shader = 0
        self.running = True

        self.width = self.window.get_width()
        self.height = self.window.get_height()


        self.data_settings = johnson.Johnson(johnson.getDD("settings.json"))
        self.data_settings_read = self.data_settings.readData()


        #BUFFER OPENGL
        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        self.projection = glm.ortho(0, self.window.get_width(), self.window.get_height(), 0, -1, 1)
        self.ubo = self.ctx.buffer(reserve=64)
        self.ubo.bind_to_uniform_block(0)
        self.ubo.write(self.projection.to_bytes())

        self.fbo_texture = self.ctx.texture((self.width, self.height), 4)
        self.fbo_texture.filter = (mgl.NEAREST, mgl.NEAREST)

        rbo_buffer = self.ctx.depth_renderbuffer((self.width, self.height))
        self.fbo_buffer = self.ctx.framebuffer(color_attachments=[self.fbo_texture], depth_attachment=rbo_buffer)

        self.ebo = self.ctx.buffer(indices)
        self.vbo = self.ctx.buffer(vertices)

        self.programs = Programs(self)
        self.program = self.programs.shader_pp
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "2f 2f", "aPos", "aTexCoords")], index_buffer=self.ebo)




        #CREATE SCENES
        self.scene_name = ""
        self.scenes = SceneManager(self)

    def getFps(self):
        return self.clock.get_fps()
       
    def closeGame(self):
        self.running = False

    def switchScene(self, scene_name: str):
        self.scene_name = scene_name


    def update(self):
        self.scenes.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.VIDEORESIZE:
                min_width, min_height = 800, 600
                new_w = max(event.w, min_width)
                new_h = max(event.h, min_height)

                #RESIZING ATTRIBUTES
                self.width, self.height = new_w, new_h

                self.ctx.viewport = (0, 0, new_w, new_h)
                self.projection = glm.ortho(0, new_w, new_h, 0, -1, 1)
                self.ubo.write(self.projection.to_bytes())

                self.window = pg.display.set_mode((new_w, new_h), flags=pg.DOUBLEBUF|pg.OPENGL|pg.RESIZABLE)

            self.scenes.event(event=event)
        
        


    def render(self):
        if self.data_settings_read["vhs-shader"]:
            self.time_fbo_shader += self.delta_time

            self.fbo_buffer.use() 
            self.fbo_buffer.clear(0.0, 0.0, 0.0, 1.0)

            self.scenes.render()

            self.ctx.screen.use()
            self.ctx.clear(0.0, 0.0, 0.0, 1.0)

            self.fbo_texture.use()

            self.program["scale"] = glm.vec2(self.width, self.height)
            self.program["tex"] = 0
            self.program["time"] = self.time_fbo_shader

            self.vao.render()
        else:
            self.scenes.render()


        pg.display.flip()


    def run(self):
        
        while self.running:
            self.delta_time = min(self.clock.tick(120) / 1000.0, 0.05)        
        
            self.update()
            self.render()

            

        self.scenes.save()
        self.data_settings.saveData(self.data_settings_read)
        pg.quit()



if __name__ == "__main__":
    game = MyGame()
    game.run()



print("FINISHED OK")
