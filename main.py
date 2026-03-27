import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from MyGame import SceneManager, johnson
import pygame as pg
import moderngl as mgl
import glm
from array import array





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

    def showMouse(self):
        pg.mouse.set_visible(False)





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

        self._ctx = mgl.create_context()
        self._ctx.enable(mgl.DEPTH_TEST)
        self._ctx.enable(mgl.BLEND)
        self._ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
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
        # ONLY ADMIN WORKPLACE
        self.data_settings = johnson.Johnson(johnson.getDD("settings.json"))
        self.data_settings_read = self.data_settings.readData()
        #--------------------------------------------------------------------------------------------------------


    

        #--------------------------------------------------------------------------------------------------------
        # OPENGL BUFFERS AND SHADER STORAGE SETTINGS
        #--------------------------------------------------------------------------------------------------------
        vertices = array("f", [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        indices = array("I", [0, 1, 2, 2, 3, 0])

        self.__projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
        self.__ubo = self._ctx.buffer(reserve=64)
        self.__ubo.bind_to_uniform_block(0)
        self.__ubo.write(self.__projection.to_bytes())

        self._ebo = self._ctx.buffer(indices)
        self._vbo = self._ctx.buffer(vertices)
        #--------------------------------------------------------------------------------------------------------

        self.request = GameRequest(self)

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
    
    def setFirst(self, scene):
        self._scene_name = scene
    

    def __update(self):
        self.__scenes.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

            self.__scenes.event(event=event)
        
        


    def __render(self):
        
        self._ctx.clear(1, 1, 1)
        self.__scenes.render()


        pg.display.flip()


    def __run(self):
        
        while self._running:
            self.delta_time = min(self.__clock.tick(120) / 1000.0, 0.05)        
        
            self.__update()
            self.__render()

            

        self.__scenes.save()
        self.data_settings.saveData(self.data_settings_read)
        pg.quit()



if __name__ == "__main__":
    game = MyGame()
    game._MyGame__run()



print("FINISHED OK")
