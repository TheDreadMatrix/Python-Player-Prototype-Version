from supermarioworld.scenes.base import EmptyScene
from supermarioworld.typing.gametype import GameType

from supermarioworld.rendering.users import FadeLabel
from supermarioworld.rendering.shaders import CustomShader

from level.world import World


# Fix spatial hash
class Level(EmptyScene):
    def onInitialization(self, game: GameType, biome: int, music_name: str):
        self.world = World(game=game, biome=biome)

        self.assets.regImage("background", "menu/background.png")

        self.fade_label = FadeLabel(game)
        self.fade_label.fadeIn(speed=0.5)

        # Fbo
        self.renderer.createFbo("background", (game.width, game.height))

        self.pixel_mosiac_shader = CustomShader(game, "vertex/vertex_1.vert", "post-processing/post-processing-pxm.frag")
     
        self.renderer.regShader("pxm", self.pixel_mosiac_shader)
      

        self.pixel_size = 128
        self.target_pixel_size = 1
        self.pixel_speed = 140

        # Audio
        self.audio.load(music_name)
        self.audio.play()

    

    def onUpdate(self):
        self.fade_label.update() 
        self.world.update()

        if self.pixel_size > self.target_pixel_size:
            self.pixel_size -= self.pixel_speed * self.game.delta_time
            self.pixel_size = max(self.pixel_size, self.target_pixel_size)
    

    def onEvent(self, event):
        self.world.handle(event=event)


    def onRender(self):
        self.renderer.beginFbo("background")

        self.world.render()

        self.renderer.endFbo()

        
        self.pixel_mosiac_shader.setUniform("pixelSize", self.pixel_size)
        self.pixel_mosiac_shader.setUniform("textureSize", (self.game.width, self.game.height))

        self.renderer.renderFbo("background", size=(self.game.width, self.game.height), shader_key="pxm")

        self.fade_label.render()

    







    