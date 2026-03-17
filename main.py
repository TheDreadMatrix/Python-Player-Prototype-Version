import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from MyGame import SceneManager
import pygame as pg
import moderngl as mgl
import glm
from array import array



class MyGame:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self.window = pg.display.set_mode((800, 600), flags=pg.DOUBLEBUF|pg.OPENGL|pg.RESIZABLE)
        pg.display.set_caption("Super Mario World: 91P Retitle")

        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.BLEND)
        self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self.ctx.viewport = (0, 0, *self.window.get_size())

        self.clock = pg.time.Clock()

        self.delta_time = 0
        self.running = True

        self.vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.indices = array("I", [0, 1, 2, 2, 3, 0])

        self.projection = glm.ortho(0, self.window.get_width(), self.window.get_height(), 0, -1, 1)
        self.ubo = self.ctx.buffer(reserve=64)
        self.ubo.bind_to_uniform_block(0)
        self.ubo.write(self.projection.to_bytes())

        self.width = self.window.get_width()
        self.height = self.window.get_height()

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

                self.width, self.height = new_w, new_h

                self.ctx.viewport = (0, 0, new_w, new_h)
                self.projection = glm.ortho(0, new_w, new_h, 0, -1, 1)
                self.ubo.write(self.projection.to_bytes())

                self.window = pg.display.set_mode((new_w, new_h), flags=pg.DOUBLEBUF|pg.OPENGL|pg.RESIZABLE)

            self.scenes.event(event=event)
        
        


    def render(self):
        self.ctx.clear(0.7, 0.7, 0.7, 1)
        self.scenes.render()
        pg.display.flip()


    def run(self):
        while self.running:
            self.delta_time = min(self.clock.tick(120) / 1000.0, 0.05)        
        
            self.update()
            self.render()

            

        self.scenes.save()
        pg.quit()



if __name__ == "__main__":
    game = MyGame()
    game.run()



print("FINISHED OK")
