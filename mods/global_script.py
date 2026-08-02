from supermarioworld.typing.gametype import GameType, BasicEvent
from supermarioworld.shaders import CustomShader, VertexAttribute
from supermarioworld.enums.controllers import Keys




game: GameType = game


crt = CustomShader(game.renderer, game.paths.ShaderText("vertex/vertex_1.vert"), game.paths.ShaderText("post-processing/post-processing-crt.frag"), attributes=[])



game.renderer.regShader("crt-shader", crt, True)
game.renderer.createFbo("fbo-shader", (game.width, game.height), True)




crt_flag = True
game.audio.setFilterLowPass(1500 if crt_flag else 20000)
time = 0 

def onUpdate():
    global time

    
    time += game.delta_time


def onEvent(event: BasicEvent):
    global crt_flag
    if game.keyboard.isDown(Keys.H, event):
        crt_flag = not crt_flag
        game.audio.setFilterLowPass(1500 if crt_flag else 20000)



def preRender():
    if crt_flag:
        game.renderer.beginFbo("fbo-shader")



def onRender():
    if crt_flag:
        game.renderer.endFbo()

        crt.setUniform("time", time)

        game.renderer.renderFbo("fbo-shader", size=(game.width, game.height), shader_key="crt-shader")