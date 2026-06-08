import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from supermarioworld.bootloder import Bootloader


from supermarioworld.core.runtime.corepaths import CorePath
from supermarioworld.core.runtime.daemonapi import GameRequest

from supermarioworld.core.player.accounts import PlayerAccountManager
from supermarioworld.core.resources import AssetsResources

from supermarioworld.core.audio import AudioStream

from supermarioworld.core.renderer import MainRenderer

import pygame as pg









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
        self._run_scene = None
        self._DEBUG = False

        self.delta_time = 0
        

        self._window = pg.display.set_mode((800, 600), flags=pg.DOUBLEBUF|pg.OPENGL)

        self.width = self._window.get_width()
        self.height = self._window.get_height()

        icon = pg.image.load(self.paths.AssetPath("icon.ico"))

        pg.display.set_caption("Super Mario World: 91 Retitle")
        pg.display.set_icon(icon)
        
        # Configuration settings
        self.account = PlayerAccountManager(self)

        # Scenes and user side
        self.assets = AssetsResources(self)
        self.audio = AudioStream(self)

        # Renderer
        self.renderer = MainRenderer(self)


  
    def _initSubstence(self):
        self._scene_name = ""

        self.router = Bootloader(self)
        self.router.onLoad(self)
        self.router.onInitScene(self)
        self.router._postInitScene()
       

        
    
    def getFps(self):
        return self._clock.get_fps()
    
    def getScene(self):
        return self._scene_name
    

    def clearColor(self, r, g, b):
        self.renderer._clearColor(r, g, b)
    

    def _update(self):
        self.router.update()


        for event in pg.event.get():
            self.router.event(event=event)

            if event.type == pg.QUIT:
                self._running = False

            if event.type == pg.VIDEORESIZE:
                self.width, self.height = event.w, event.h

                self.renderer._eventResize()

            
        
        


    def _render(self):
        self.renderer._clearColor(0.7, 0.6, 0.8)

        self.router.render()
       
        pg.display.flip()
        


    def _run(self):
        while self._running:
            self.delta_time = min(self._clock.tick(self.account.getFps()) / 1000.0, 0.02)        
        
            self._update()
            self._render()

            

        self.router.save()
        
        self.account.save()
        pg.quit()



