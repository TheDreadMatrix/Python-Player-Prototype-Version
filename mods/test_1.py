from supermarioworld.typing.gametype import GameType
from supermarioworld.rendering.shaders import CustomShader
from supermarioworld.enums.controllers import Keys
import supermarioworld

game: GameType
print(supermarioworld.__file__)

crt = CustomShader(game, "vertex/vertex_1.vert", "post-processing/post-processing-crt.frag")



game.renderer.regShader("crt-shader", crt, True)
game.renderer.createFbo("fbo-shader", (game.width, game.height), True)

game.audio.setFilterLowPass(1500)




time = 0 

def onUpdate():
    global time

    time += game.delta_time * 20


def preRender():
    game.renderer.beginFbo("fbo-shader")



def onRender():
    game.renderer.endFbo()

    crt.setUniform("time", time)

    game.renderer.renderFbo("fbo-shader", size=(game.width, game.height), shader_key="crt-shader")