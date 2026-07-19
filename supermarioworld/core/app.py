import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


from supermarioworld.core.router import SceneManager


from supermarioworld.core.runtime.corepaths import CorePath
from supermarioworld.core.runtime.daemonapi import GameRequest
from supermarioworld.core.runtime.settings import Settings

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
        self.game = game

        language_key = language_key.lower()

        if language_key not in self.AVAILABLE_LANGUAGES:
            language_key = "en"


        self.language_data = readData(game.paths.ConfigPath(f"locale/{language_key}.json"))


    def switchLanguage(self, language_key: str):
        language_key = language_key.lower()

        if language_key not in self.AVAILABLE_LANGUAGES:
            language_key = "en"

        self.language_data = readData(self.game.paths.ConfigPath(f"locale/{language_key}.json"))


    def gettext(self, word_key):
        return self.language_data.get(word_key, word_key)








class SuperMariWorldApplication:
    def __init__(self, file_execution: str, project_name: str, use_resizeble=False, vendor_size=(780, 580), title="Super Martis World 91"):
        self.PROJECT_NAME = project_name
        
        # Runtime
        self.request = GameRequest(self)
        self.paths = CorePath(file_execution=file_execution)
        self.settings = Settings(project_name)
        


        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        
        flags = pg.DOUBLEBUF|pg.OPENGL  
        if use_resizeble:
            flags |= pg.RESIZABLE

        self._window = pg.display.set_mode(vendor_size, flags=flags)

        self.width = self._window.get_width()
        self.height = self._window.get_height()

        icon = pg.image.load(self.paths.AssetPath("icon.ico"))

        pg.display.set_caption(title)
        pg.display.set_icon(icon)
        
        # Configuration settings 
        self.account = PlayerAccountManager(self)
        self._locale = Locale(game=self, language_key=self.account.getLanguage())
        self._locale_key = self.account.getLanguage()
        

        # Attributes
        self._clock = pg.time.Clock()
        self._running = True
        self._focused = True

        
        self.DEBUG = False

        self.delta_time = 0
        self.tick_time = 1 / self.account.getFps()

        # Scenes and user side
        self.assets = AssetsResources(self)
        self.audio = AudioStream(self)

        # Renderer
        self.renderer = MainRenderer(self)


        # Scenes
        self.assets.beginScene("GLOBAL-DAEMON")

        for name, path in self.settings.ATLASES.items():
            self.assets.regAtlas(name, path)

        for name, path in self.settings.FONTS.items():
            self.assets.regFont(name, path)

        for name, path in self.settings.MUSIC.items():
            self.assets.regMusic(name, path)

        for name, path in self.settings.SOUNDS.items():
            self.assets.regSound(name, path)


        self.SCENA_DATA = {}

        self.router = SceneManager(self)

        

    @property
    def locale(self):
        lang = self.account.getLanguage()

        if self._locale_key != lang:
            self._locale_key = lang
            self._locale.switchLanguage(lang)

        return self._locale
       
    @property
    def player(self):
        return self.account.current_account
    
    
    def getFps(self):
        return self._clock.get_fps()
    

    def clearColor(self, r, g, b):
        self.renderer._clearColor(r, g, b)
    

    def _update(self):
        if self._focused:        
            self.router.update()
    
            


        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F3:
                    self.DEBUG = not self.DEBUG

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



