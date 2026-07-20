from supermarioworld.scenes.base import EmptyScene
from supermarioworld.typing.gametype import GameType

from supermarioworld.rendering.users import TextLabel, FadeLabel
from supermarioworld.rendering.shaders import CustomShader
from supermarioworld.camera import Camera

from overworld.overworld_tilemap import OverWorldMap
from overworld.overworld_entities import OverWorldPlayer


import pygame as pg




class Overworld(EmptyScene):      
    def onInitialization(self, game: GameType, map_ref: str, biome: int, music_name: str):


        # overworld player
        self.player = OverWorldPlayer(game, map_ref=map_ref, move_speed=self.WALK_SPEED)


        # Tile map
        self.overworld_map = OverWorldMap(game=game, notation_file=f"overworld/notations/{self.NOTATION_BIOME_OVERWORLD.get(biome)}.json")
        self.overworld_map.load(map_ref)

  
        # Camera
        self.camera = Camera(screen_width=game.width, screen_height=game.height, smooth=self.SMOOTH_CAMERA)
        self.camera.setBounds(0, -80, 2500, 2500)
      

       
        # Ui
        self.assets.regImage("overworld-border", "overworld/overworld-border.png")
        self.assets.regCutOutImage("x-lives", atlas_key="fonts", x=313, y=113, w=7, h=7)


        self.text_titles = TextLabel(game,  font_key="pixel", size_font=18)
        self.text_account = TextLabel(game,  text=f"#P-{self.game.player.getSlot()}", font_key="pixel", size_font=15, r=0, g=0, b=0)
        self.text_points = TextLabel(game,  text=self.locale.gettext("main-pointer-overworld"), font_key="pixel", size_font=13, r=0, g=0, b=0)
        self.text_lives = TextLabel(game,  text=f"{self.game.player.lives}", font_key="pixel", size_font=18, r=0, g=0, b=0)

        self.text_fps = TextLabel(game, text=f"FPS: {self.account.getFps()}/{self.account.getFps()}", font_key="pixel", size_font=15)
        self.fps_timer = 0

        # Fade
        self.OUT_FADE = False
        self.fade_label = FadeLabel(game=game)
        self.fade_label.fadeIn(speed=1.5)

        # Pixel mosaic
        self.pixel_size = 1
        self.target_pixel_size = 1

       
        self.pixel_mosiac_shader = CustomShader(game, "vertex/vertex_1.vert", "post-processing/post-processing-pxm.frag")

        self.renderer.regShader("pxm", self.pixel_mosiac_shader)
        self.renderer.createFbo("tile-map", (game.width, game.height))
        
        # Audio
        self.open_egg_sound = self.audio.giveSound("open-egg")
        self.sound_choose = game.audio.giveSound("choose")
        self.sound_exit = game.audio.giveSound("pause")

        self.audio.load(music_name)
        self.audio.play(loop=True)

        


    def onUpdate(self):
        # Fade
        self.fade_label.update()

        # Camera
        self.camera.update(delta_time=self.game.delta_time, target_x=self.player.position[0], target_y=self.player.position[1])

        # Overworld spatial
        self.player.updatePlayer(sound_if_passed=self.sound_choose)

        self.overworld_map.update(*self.player.position)
        
        

        # Pixel mosaic
        if self.player.redirecting:
            self.target_pixel_size = 128
        else:
            self.target_pixel_size = 1

        

        if self.pixel_size < self.target_pixel_size:
            self.pixel_size += self.PIXEL_SPEED * self.game.delta_time
            self.pixel_size = min(self.pixel_size, self.target_pixel_size)

        elif self.pixel_size > self.target_pixel_size:
            self.pixel_size -= self.PIXEL_SPEED * self.game.delta_time
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
        title = self.locale.gettext(self.player._getTitleNode())
        if self.text_titles.text != title:
            self.text_titles.setText(title)

        
    

    def onEvent(self, event):
        if event.type == pg.KEYDOWN and self.game.DEBUG:
            if event.key == pg.K_l:
                self.request.restartScene()

        self.player.handleEventNodes(event=event, sound_if_exit=self.sound_exit)
        
        
    

    def onRender(self):

        # Render map
        self.renderer.beginFbo("tile-map")

        self.overworld_map.renderMap(self.camera)

  
        self.renderer.endFbo()

        self.pixel_mosiac_shader.setUniform("pixelSize", self.pixel_size)
        self.pixel_mosiac_shader.setUniform("textureSize", (self.game.width, self.game.height))

        self.renderer.renderFbo("tile-map", size=(self.game.width, self.game.height), shader_key="pxm")


        # Render player
        self.player.renderPlayer(self.camera)

        
        # Render UI
        self.renderer.render("overworld-border", size=(self.game.width, self.game.height))
        self.renderer.render("x-lives", size=(20, 20), position=(155, 70))

        title_size = self.text_titles.size

        max_width = 400

        scale = 1.0
        if title_size[0] > max_width:
            scale = max_width / title_size[0]

        render_size = (title_size[0] * scale, title_size[1] * scale)

        self.renderer.render(self.text_titles.texture_id, size=render_size, position=(245, 70))
        self.renderer.render(self.text_lives.texture_id, size=self.text_lives.size, position=(185, 70))

        

        
        self.renderer.render(self.text_account.texture_id, size=self.text_account.size, position=(25, self.game.height - 25))
        self.renderer.render(self.text_points.texture_id, size=self.text_points.size, position=(60, 495))

        if self.game.DEBUG:
            self.renderer.render(self.text_fps.texture_id, size=self.text_fps.size, position=(25, 25))

        self.fade_label.render()

        


    
