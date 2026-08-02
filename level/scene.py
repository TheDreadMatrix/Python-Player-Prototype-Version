from supermarioworld.scenes.base import EmptyScene
from supermarioworld.typing.gametype import GameType

from supermarioworld.users import FadeLabel, TextLabel
from supermarioworld.shaders import CustomShader


from level.world import World


# Fix spatial hash
class Level(EmptyScene):
    def onInitialization(self, game: GameType, biome: int, music_name: str):
        self.world = World(game=game, biome=biome)

        self.assets.regImage("background", "menu/background.png")

        self.fade_label = FadeLabel(game)
        self.fade_label.fadeIn(speed=0.5)

        self.time_label = TextLabel(game, f"TIME: {self.world.time}", font_key="pixel")
        self.time_label.position = (0, 50)

        # Fbo
        self.renderer.createFbo("background", (game.width, game.height))

        self.pixel_mosiac_shader = CustomShader(game.renderer, 
                                                game.paths.ShaderText("vertex/vertex_1.vert"), 
                                                game.paths.ShaderText("post-processing/post-processing-pxm.frag"))
     
        self.renderer.regShader("pxm", self.pixel_mosiac_shader)
      

        self.pixel_size = 128
        self.target_pixel_size = 1
        self.pixel_speed = 140

        self.death_started = False

        # Audio
        self.audio.load(music_name)
        self.audio.play()


    

    def onUpdate(self):
        self.world.update()

        self.fade_label.update()
        self.time_label.setText(f"TIME: {int(self.world.time)}")

        

        if self.pixel_size > self.target_pixel_size:
            self.pixel_size -= self.pixel_speed * self.game.delta_time
            self.pixel_size = max(self.pixel_size, self.target_pixel_size)

        if self.world.main.death_timer >= 4.5 and not self.death_started:
            self.fade_label.fadeOut(0.5)
            self.death_started = True

        if self.world.main.death_timer >= 8.5:
            self.game.router.redirect(self.game.player.current_overworld)
        
    

    def onEvent(self, event):
        self.world.handle(event=event)


    def onRender(self):
        self.renderer.beginFbo("background")

        self.world.render()

        self.renderer.endFbo()

        
        self.pixel_mosiac_shader.setUniform("pixelSize", self.pixel_size)
        self.pixel_mosiac_shader.setUniform("textureSize", (self.game.width, self.game.height))

        self.renderer.renderFbo("background", size=(self.game.width, self.game.height), shader_key="pxm")

        self.time_label.render()

        self.fade_label.render()

    







    