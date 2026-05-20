import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from supermarioworld.router import SceneManager
from supermarioworld.johnson import Johnson


from supermarioworld.core.corepaths import CorePath
from supermarioworld.core.daemonapi import GameRequest
from supermarioworld.core.resources import AssetsResources, AudioStream

import pygame as pg
import moderngl as mgl
import glm



from array import array



class SuperMariWorldApplication:
    def __init__(self, file_execution: str):
        self.request = GameRequest(self)
        self.paths = CorePath(file_execution=file_execution)
        


        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self._clock = pg.time.Clock()
        self._running = True

        self.delta_time = 0
        

        self._window = pg.display.set_mode((800, 600), flags=pg.DOUBLEBUF|pg.OPENGL)
        icon = pg.image.load(self.paths.AssetPath("icon.jpg"))

        pg.display.set_caption("Super Mario World: 91 Retitle")
        pg.display.set_icon(icon)
        
        
        # Create render context
        self._ctx = mgl.create_context()
        self._ctx.enable(mgl.BLEND)
        self._ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)

        self.width = self._window.get_width()
        self.height = self._window.get_height()
        
        self._viewport = (0, 0, self.width, self.height)
        self._ctx.viewport = (0, 0, self.width, self.height)


        vertices_only = array("f", [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        self._projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
        

        self._ubo = self._ctx.buffer(reserve=64)
        self._ubo.bind_to_uniform_block(0)
        self._ubo.write(self._projection.to_bytes())

        self._ebo = self._ctx.buffer(indices)
        self._vbo = self._ctx.buffer(vertices)
        self._vbo_only = self._ctx.buffer(vertices_only)

  
        # Configuration settings
        self.settings = Johnson(self.paths.CsavesPath("settings.json"))
        self.settings_read = self.settings.readData()

        # Scenes and user side
        self.assets = AssetsResources(self)
        self.audio = AudioStream(self.assets)

        self._scene_name = ""
        self._scenes = SceneManager(self)
        self._scenes.onLoad(self)
       

        
    
    def getFps(self):
        return self._clock.get_fps()
    
    def getScene(self):
        return self._scene_name
    

    def clearColor(self, r, g, b):
        self._ctx.clear(r, g, b)
    

    def _update(self):
        self._scenes.update()


        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

            if event.type == pg.VIDEORESIZE:
                self.width, self.height = event.w, event.h
                

                self._projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
                self._ubo.write(self._projection.to_bytes())

                
            self._scenes.event(event=event)
        
        


    def _render(self):
        self._ctx.clear(0, 0, 0)
        self._scenes.render()
       
        pg.display.flip()
        


    def _run(self):
        while self._running:
            self.delta_time = min(self._clock.tick(self.settings_read["frametime"]) / 1000.0, 0.02)        
        
            self._update()
            self._render()

            

        self._scenes.save()
        self.settings.saveData(self.settings_read)
        pg.quit()



