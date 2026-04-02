import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from MyGame import SceneManager, johnson
import pygame as pg
import moderngl as mgl
import glm
from array import array
import sys
from pathlib import Path





class GameRequest:
    def __init__(self, game: "MyGame"):
        self.__game = game

    def setShaderVhs(self, flag):
        pass

    def setAudioVhs(self, flag):
        pass

    def redirectScene(self, scene):
        self.__game._scene_name = scene

    def closeGame(self):
        self.__game._running = False

    def showMouse(self, flag):
        pg.mouse.set_visible(flag)


class CorePath:
    def __init__(self, base_dir=None):
        if base_dir:
            self._runtime_dir = Path(base_dir)
        else:
            if getattr(sys, "frozen", False):
                self._runtime_dir = Path(r"C:\Users\User\.vscode\KartoshkaGame")
            else:
                self._runtime_dir = Path(__file__).resolve().parent

        if hasattr(sys, "_MEIPASS"):
            self._resource_dir = Path(sys._MEIPASS)
        else:
            self._resource_dir = self._runtime_dir

        self._assets_dir = self._resource_dir / "assets"
        self._shaders_dir = self._resource_dir / "shaders"
        self._soundtracks_dir = self._resource_dir / "soundtracks"

        self._data_dir = self._runtime_dir / "data"

    def _ensure_file(self, path: Path, kind: str) -> Path:
        if not path.exists():
            raise FileNotFoundError(f"{kind} file not found: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"{kind} is not a file: {path}")
        return path

    def ShaderPath(self, filename):
        return str(self._ensure_file(self._shaders_dir / filename, "Shader"))

    def AssetPath(self, filename):
        return str(self._ensure_file(self._assets_dir / filename, "Asset"))

    def DataPath(self, filename):
        return str(self._ensure_file(self._data_dir / filename, "Data"))

    def SoundtrackPath(self, filename):
        return str(self._ensure_file(self._soundtracks_dir / filename, "Soundtrack"))

    def ShaderText(self, filename):
        path = self._ensure_file(self._shaders_dir / filename, "Shader")
        return path.read_text(encoding="utf-8")

    def AssetDir(self):
        return str(self._assets_dir)

    def ShaderDir(self):
        return str(self._shaders_dir)

    def DataDir(self):
        return str(self._data_dir)

    def SoundtrackDir(self):
        return str(self._soundtracks_dir)






class MyGame:
    def __init__(self):
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        # INIT ATTRIBUTE AND OPENGL SYSTEM
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self.__window = pg.display.set_mode((800, 600), flags=pg.DOUBLEBUF|pg.OPENGL)
        pg.display.set_caption("Super Mario World: 91P Retitle")
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        
        

        self._ctx = mgl.create_context()
        self._ctx.enable(mgl.BLEND)
        self._ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self._ctx.enable(mgl.DEPTH_TEST)
        self._ctx.viewport = (0, 0, self.__window.get_width(), self.__window.get_height())
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------


        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        # FRAMERATE AND RUNNING ATTRIBUTES
        self.__clock = pg.time.Clock()
        self._running = True
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        # FREE TO USE
        self.delta_time = 0
        self.width = self.__window.get_width()
        self.height = self.__window.get_height()
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------


        #--------------------------------------------------------------------------------------------------------
        # OPENGL BUFFERS AND SHADER STORAGE SETTINGS
        #--------------------------------------------------------------------------------------------------------
        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        vertices_only = array("f", [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        self.__projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
        self.__ubo = self._ctx.buffer(reserve=64)
        self.__ubo.bind_to_uniform_block(0)
        self.__ubo.write(self.__projection.to_bytes())

        self._ebo = self._ctx.buffer(indices)
        self._vbo = self._ctx.buffer(vertices)
        self._vbo_only = self._ctx.buffer(vertices_only)
        #--------------------------------------------------------------------------------------------------------

        self.request = GameRequest(self)
        self.paths = CorePath()

        icon = pg.image.load(str(self.paths._resource_dir / "icon.ico"))
        pg.display.set_icon(icon)
        
        #--------------------------------------------------------------------------------------------------------
        # ONLY ADMIN WORKPLACE
        self.data_settings = johnson.Johnson(self.paths.DataPath("settings.json"))
        self.data_settings_read = self.data_settings.readData()
        #--------------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        # ALL SCENES REGISTERS IN THAT
        self._scene_name = ""
        self.__scenes = SceneManager(self)
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------


    def getFps(self):
        return self.__clock.get_fps()
    
    def getScene(self):
        return self._scene_name
    

    def setColorScreen(self, r, g, b):
        self._ctx.clear(r, g, b)
    

    def __update(self):
        self.__scenes.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and self.data_settings_read["escape-with-esc"]:
                    self._running = False

            self.__scenes.event(event=event)
        
        


    def __render(self):
        self._ctx.clear(1, 1, 1)
        self.__scenes.render()
        pg.display.flip()


    def __run(self):
        while self._running:
            self.delta_time = min(self.__clock.tick(240) / 1000.0, 0.05)        
        
            self.__update()
            self.__render()

            

        self.__scenes.save()
        self.data_settings.saveData(self.data_settings_read)
        pg.quit()



if __name__ == "__main__":
    game = MyGame()
    game._MyGame__run()



print("FINISHED OK")
