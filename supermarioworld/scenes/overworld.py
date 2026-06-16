from supermarioworld.scenes.base import EmptyScene
from supermarioworld.package_typing import GameType

from supermarioworld.tilemaps.overworld_tilemap import OverWorldMap
from supermarioworld.entities.overworld_entities import OverWorldPlayer

from supermarioworld.rendering.users import TextLabel, FadeLabel
from supermarioworld.rendering.shaders import CustomShader
from supermarioworld.camera import Camera

from supermarioworld.configuration import NOTATION_BIOME_OVERWORLD




class OverWorld(EmptyScene):
    def __init__(self, game: GameType, biome: int, music_name: str, map_ref: str):
        super().__init__(game)

        # Audio
        self.audio.load(music_name)
        self.audio.play(loops=-1, fade_in=2000)

    

        # overworld player
        self.player = OverWorldPlayer(game, map_ref=map_ref)

        

        # Tile map
        self.overworld_map = OverWorldMap(game=game, notation_file=f"overworld/notations/{NOTATION_BIOME_OVERWORLD.get(biome)}.json")
        self.overworld_map.load(map_ref)

        x, y = game.player.current_overworld_camera_pos
  
        # Camera
        self.camera = Camera(game=game, screen_width=game.width, screen_height=game.height, smooth=0.7, x=x, y=y)
        self.camera.setBounds(0, -80, 2500, 2500)

       
        # Ui
        self.assets.regImage("overworld-border", "overworld/overworld-border.png")

        self.text_titles = TextLabel(game, "titles", font_key="pixel", size_font=18)
        self.text_account = TextLabel(game, "text-account", f"#P-{self.game.player.getSlot()}", font_key="pixel", size_font=15)
        self.text_points = TextLabel(game, "text-points", text="MOVING: 'WASD', SELECT: 'Q', EXIT TO MENU: 'E'", font_key="pixel", size_font=15)
        self.text_lives = TextLabel(game, "text-lies", text=f"{self.game.player.lives}", font_key="pixel", size_font=18)

        self.text_fps = TextLabel(game, "text-fps", text=f"FPS: {self.account.getFps()}/{self.account.getFps()}", font_key="pixel", size_font=15)
        self.fps_timer = 0

        # Fade
        self.OUT_FADE = False
        self.fade_label = FadeLabel(game=game)
        self.fade_label.fadeIn(speed=1.5)

        # Pixel mosaic
        self.pixel_size = 1
        self.target_pixel_size = 1
        self.pixel_speed = 60

        self.renderer.createFbo("tile-map", (game.width, game.height))


        self.pixel_mosiac_shader = CustomShader(game, "testing/default.vert", "post-processing/post-processing-pxm.frag")
        self.pixel_mosiac_shader.defineUniform("pixel_size", "pixelSize")
        self.pixel_mosiac_shader.defineUniform("texture_size", "textureSize")

        self.renderer.regShader("pxm", self.pixel_mosiac_shader)
        
        


    def onUpdate(self):
        

        # Fade
        self.fade_label.update()

        # Overworld spatial
        self.overworld_map.update(self.player)
        
        # Camera
        self.camera.follow(self.player.position[0], self.player.position[1])

        # Pixel mosaic
        if self.player.redirecting and self.player.redirect_scene != "base:menu":
            self.target_pixel_size = 128
        else:
            self.target_pixel_size = 1

        

        if self.pixel_size < self.target_pixel_size:
            self.pixel_size += self.pixel_speed * self.game.delta_time
            self.pixel_size = min(self.pixel_size, self.target_pixel_size)

        elif self.pixel_size > self.target_pixel_size:
            self.pixel_size -= self.pixel_speed * self.game.delta_time
            self.pixel_size = max(self.pixel_size, self.target_pixel_size)

        # Fps
        self.fps_timer += self.game.delta_time
        if self.fps_timer >= 1.5:
            self.text_fps.setText(f"FPS: {int(self.game.getFps())}/{self.account.getFps()}")
            self.fps_timer = 0


        
        # Fade out effect
        if self.player.redirecting and not self.OUT_FADE:
            self.audio.fadeOut(2000)
            self.fade_label.fadeOut(speed=1.5)
            self.OUT_FADE = True

        # If we coming to new node
        if self.text_titles.text != self.player._getTitleNode():
            self.text_titles.setText(self.player._getTitleNode())

        self.player.updatePlayer(self.camera, self.game.delta_time)
    

    def onEvent(self, event):
        if event.type == 768 and self.game.DEBUG:
            if event.key == 108:
                self.request.restartScene()
        self.player.handleEventNodes(event=event)
        
        
    

    def onRender(self):

        # Render map
        if self.player.redirecting:
            self.renderer.beginFbo("tile-map")

        self.overworld_map.renderMap(self.camera)

        if self.player.redirecting:
            self.renderer.endFbo()

            self.pixel_mosiac_shader.setUniformByOneTime("pixel_size", self.pixel_size)
            self.pixel_mosiac_shader.setUniformByOneTime("texture_size", (self.game.width, self.game.height))

            self.renderer.renderFbo("tile-map", size=(self.game.width, self.game.height), shader_key="pxm")


        # Render player
        self.player.renderPlayer(self.camera)

        
        # Render UI
        self.renderer.render("overworld-border", size=(self.game.width, self.game.height))
        self.renderer.render(self.text_titles.texture_id, size=self.text_titles.size, position=(265, 70))
        self.renderer.render(self.text_lives.texture_id, size=self.text_lives.size, position=(185, 70))

        

        
        self.renderer.render(self.text_account.texture_id, size=self.text_account.size, position=(25, self.game.height - 25))
        self.renderer.render(self.text_points.texture_id, size=self.text_points.size, position=(65, 495))

        if self.game.DEBUG:
            self.renderer.render(self.text_fps.texture_id, size=self.text_fps.size, position=(25, 25))

        self.fade_label.render()


    

    def onSave(self):
        self.renderer.deleteFbo("tile-map")

        self.renderer.delShader("pxm")
        
        self.overworld_map.delRes()

        self.text_account.delRes()
        self.text_fps.delRes()
        self.text_lives.delRes()
        self.text_points.delRes()
        self.text_titles.delRes()

        self.assets.delImage("overworld-border")
        
        self.player.deletePlayerRes()
    
