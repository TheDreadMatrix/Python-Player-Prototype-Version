import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from supermarioworld.bootloder import Bootloader


from supermarioworld.core.runtime.corepaths import CorePath
from supermarioworld.core.runtime.daemonapi import GameRequest

from supermarioworld.core.accounts import PlayerAccountManager
from supermarioworld.core.resources import AssetsResources

from supermarioworld.core.audio.audio import AudioStream

from supermarioworld.core.renderer import MainRenderer

import pygame as pg



from supermarioworld.johnson import readData


class Locale:
    AVAILABLE_LANGUAGES = {
        "ru",
        "en"
    }
    def __init__(self, game: "SuperMariWorldApplication", language_key: str):
        language_key = language_key.lower()

        if language_key not in self.AVAILABLE_LANGUAGES:
            print(f"[Locale] Unknown language '{language_key}', fallback to 'en'")
            language_key = "en"


        self.language_data = readData(game.paths.ConfigPath(f"locale/{language_key}.json"))


    def gettext(self, word_key):
        return self.language_data.get(word_key, "Undefined translation")





class SuperMariWorldApplication:
    def __init__(self, file_execution: str):
        
        # Runtime
        self.request = GameRequest(self)
        self.paths = CorePath(file_execution=file_execution)
        


        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        

        self._window = pg.display.set_mode((700, 580), flags=pg.DOUBLEBUF|pg.OPENGL|pg.RESIZABLE)

        self.width = self._window.get_width()
        self.height = self._window.get_height()

        icon = pg.image.load(self.paths.AssetPath("icon.ico"))

        pg.display.set_caption("Super Martis World 91")
        pg.display.set_icon(icon)
        
        # Configuration settings 
        self.account = PlayerAccountManager(self)
        

        # Attributes
        self._clock = pg.time.Clock()
        self._running = True
        self._focused = True

        
        self._run_scene = None
        self._DEBUG = True if os.getenv("DAEMON_SMW_DEBUG") else False 

        self.delta_time = 0
        self.tick_time = 1 / self.account.getFps()

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

    @property
    def locale(self):
        return Locale(game=self, language_key=self.account.getLanguage())
       
    @property
    def player(self):
        return self.account.current_account
    
    @property
    def DEBUG(self):
        return self._DEBUG
    
    def getFps(self):
        return self._clock.get_fps()
    
    def getScene(self):
        return self._scene_name
    

    def clearColor(self, r, g, b):
        self.renderer._clearColor(r, g, b)
    

    def _update(self):
        if self._focused:        
            self.router.update()
    
            


        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F3:
                    self._DEBUG = not self._DEBUG

            elif event.type == pg.WINDOWFOCUSLOST:
                self.audio.pause()
                self._focused = False

            elif event.type == pg.WINDOWFOCUSGAINED:
                self.audio.unpause()
                self._focused = True

            if self._focused:
                self.router.event(event=event)

            if event.type == pg.QUIT:
                self._running = False

            if event.type == pg.VIDEORESIZE:
                self.width, self.height = event.w, event.h

                self.renderer._eventResize()


            
        
        


    def _render(self):
        if not self._focused:
            return
    
        self.renderer._clearColor(0, 0, 0)

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



