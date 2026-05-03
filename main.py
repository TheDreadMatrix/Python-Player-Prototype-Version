import os
print(os.getenv("APPDATA"))
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from supermarioworld.router import SceneManager
from supermarioworld.johnson import Johnson

import pygame as pg
import moderngl as mgl
import glm


import sys
from array import array
from pathlib import Path





class GameRequest:
    def __init__(self, game: "MyGame"):
        self._game = game

    def restartScene(self):
        pass

    def redirectScene(self, scene):
        self._game._scene_name = scene

    def closeGame(self):
        self._game._running = False



class CorePath:
    def __init__(self, base_dir=None):
        if base_dir:
            self._runtime_dir = Path(base_dir)
        else:
            if getattr(sys, "frozen", False):
                self._runtime_dir = Path(os.getenv("APPDATA")) / ".superkartoshkaworld"
            else:
                self._runtime_dir = Path(__file__).resolve().parent / "assets"

        if hasattr(sys, "_MEIPASS"):
            self._resource_dir = Path(sys._MEIPASS) / "assets"
        else:
            self._resource_dir = self._runtime_dir 


        self._assets_dir = self._resource_dir / "images"
        self._shaders_dir = self._resource_dir / "shaders"
        self._music_dir = self._resource_dir / "music"
        self._sound_dir = self._resource_dir / "sounds"

        
        self._config_dir = self._runtime_dir / "config"
        self._csaves_dir = self._runtime_dir / "csaves"


    def _ensure_file(self, path: Path, kind: str) -> Path:
        if not path.exists():
            raise FileNotFoundError(f"{kind} file not found: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"{kind} is not a file: {path}")
        return path
    

    def ConfigPath(self, filename):
        return str(self._ensure_file(self._config_dir / filename, "Config"))
    
    def CsavesPath(self, filename):
        return str(self._ensure_file(self._csaves_dir / filename, "Csaves"))
    
    def DataPath(self, filename):
        return "NOT WORKING"
    

    
    def AssetPath(self, filename):
        return str(self._ensure_file(self._resource_dir / filename, "Assets"))

    def ShaderPath(self, filename):
        return str(self._ensure_file(self._shaders_dir / filename, "Shader"))

    def ImagesPath(self, filename):
        return str(self._ensure_file(self._assets_dir / filename, "Images"))

    def MusicPath(self, filename):
        return str(self._ensure_file(self._music_dir / filename, "Music"))

    def SoundPath(self, filename):
        return str(self._ensure_file(self._sound_dir / filename, "Sound"))

    def ShaderText(self, filename):
        path = self._ensure_file(self._shaders_dir / filename, "Shader")
        return path.read_text(encoding="utf-8")

  






class MyGame:
    def __init__(self):
        self.request = GameRequest(self)
        self.paths = CorePath()


        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self._window = pg.display.set_mode((800, 600), flags=pg.DOUBLEBUF|pg.OPENGL|pg.RESIZABLE)
        icon = pg.image.load(self.paths.AssetPath("icon.ico"))

        pg.display.set_caption("Super Mario World: 91 Retitle")
        pg.display.set_icon(icon)
        
        

        self._ctx = mgl.create_context()
        self._ctx.enable(mgl.BLEND)
        self._ctx.enable(mgl.DEPTH_TEST)
        self._ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self._ctx.viewport = (0, 0, self._window.get_width(), self._window.get_height())


        self._clock = pg.time.Clock()
        self._running = True


        self.delta_time = 0
        self.width = self._window.get_width()
        self.height = self._window.get_height()


        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        self._projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
        self._ubo = self._ctx.buffer(reserve=64)
        self._ubo.bind_to_uniform_block(0)
        self._ubo.write(self._projection.to_bytes())

        self._ebo = self._ctx.buffer(indices)
        self._vbo = self._ctx.buffer(vertices)

  
        self.settings = Johnson(self.paths.CsavesPath("settings.json"))
        self.settings_read = self.settings.readData()


        self._scene_name = ""
        self._scenes = SceneManager(self)
    


    def getFps(self):
        return self.__clock.get_fps()
    
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
                self.width = self._window.get_width()
                self.height = self._window.get_height()
                self._projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
                self._ubo.write(self._projection.to_bytes())
                
            self._scenes.event(event=event)
        
        


    def _render(self):
        self._ctx.clear(1, 1, 1)
        self._scenes.render()
        pg.display.flip()
        


    def _run(self):
        while self._running:
            self.delta_time = min(self._clock.tick(240) / 1000.0, 0.02)        
        
            self._update()
            self._render()

            

        self._scenes.save()
        self.settings.saveData(self.settings_read)
        pg.quit()



if __name__ == "__main__":
    game = MyGame()
    game._run()



print("FINISHED OK")
