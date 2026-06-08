from supermarioworld.scenes.base import EmptyScene

from supermarioworld.tilemaps.overworld_tilemap import OverWorldMap
from supermarioworld.entities.overworld_entities import OverWorldPlayer

from supermarioworld.rendering.users import TextLabel, FadeLabel
from supermarioworld.camera import Camera


class OverWorld(EmptyScene):
    def __init__(self, game, biome: str, music_name: str, map_ref: str, clear_color: tuple=(0, 0, 0)):
        super().__init__(game)

        self.r, self.g, self.b = clear_color
        self.DEBUG = self.account.getDebug()

        # Audio
        self.audio.load(music_name)
        self.audio.play(loops=-1, fade_in=2000)

        

        BASE_BIOME_DICT = {
            0: "tile-notation-valley",
            1: "tile-notation-underground",
            2: "tile-notation-red-forest",
            3: "tile-notation-magma",
            4: "tile-notation-special"
        }

        # overworld player
        self.player = OverWorldPlayer(game, map_ref=map_ref)

        # Tile map
        self.overworld_map = OverWorldMap(game=game, notation_file=f"overworld/notations/{BASE_BIOME_DICT.get(biome)}.json")
        self.overworld_map.load(map_ref)

        x, y = self.player.account.getCurrentPlayer().current_overworld_camera_pos

        # Camera
        self.camera = Camera(game=game, screen_width=game.width, screen_height=game.height, smooth=0.7, x=x, y=y)
        self.camera.setBounds(0, -80, 2500, 2500)

       
        # Ui
        self.assets.regImage("overworld-border", "overworld/overworld-border.png")

        self.text_titles = TextLabel(game, "titles", font_key="pixel", size_font=18)
        self.text_account = TextLabel(game, "text-account", f"#PLAYER-ACCOUNT-SLOT - {self.account.getCurrentPlayer().getSlot()}", font_key="pixel", size_font=15)
        self.text_points = TextLabel(game, "text-points", text="MOVING: 'WASD', SELECT: 'Q', EXIT TO MENU: 'E'", font_key="pixel", size_font=15)
        self.text_lives = TextLabel(game, "text-lies", text=f"x{self.player.account.getCurrentPlayer().lives}", font_key="pixel", size_font=18)

        self.text_fps = TextLabel(game, "text-fps", text=f"FPS: 140", font_key="pixel", size_font=15)
        self.fps_timer = 0

        self.OUT_FADE = False
        self.fade_label = FadeLabel(game=game)
        self.fade_label.fadeIn(speed=1.5)
     


    def onUpdate(self):
        self.overworld_map.update(self.player)
        self.camera.follow(self.player.position[0], self.player.position[1])

        self.fps_timer += self.game.delta_time
        if self.fps_timer >= 1.5:
            self.text_fps.setText(f"FPS: {int(self.game.getFps())}")
            self.fps_timer = 0

        self.fade_label.update()
        
        # Fade out effect
        if self.player.redirecting and not self.OUT_FADE:
            self.audio.fadeOut(800)
            self.fade_label.fadeOut(speed=1.5)
            self.OUT_FADE = True

        # If we coming to new node
        if self.text_titles.text != self.player._getTitleNode():
            self.text_titles.setText(self.player._getTitleNode())

        self.player.updatePlayer(self.camera, self.game.delta_time)
    

    def onEvent(self, event):
        self.player.handleEventNodes(event=event)
        
    

    def onRender(self):
        self.game.clearColor(self.r, self.g, self.b)

    
        self.overworld_map.renderMap(self.camera)

        self.player.renderPlayer(self.camera)

        self.renderer.render("overworld-border", size=(self.game.width, self.game.height))
        self.renderer.render(self.text_titles.texture_id, size=self.text_titles.size, position=(265, 70))
        self.renderer.render(self.text_lives.texture_id, size=self.text_lives.size, position=(185, 70))

        if self.DEBUG:
            self.renderer.render(self.text_account.texture_id, size=self.text_account.size, position=(65, 520))
            self.renderer.render(self.text_points.texture_id, size=self.text_points.size, position=(65, 495))
            self.renderer.render(self.text_fps.texture_id, size=self.text_fps.size, position=(165, 10))

        self.fade_label.render()
    

    def onSave(self):
        self.overworld_map.delRes()

        self.assets.delImage("overworld-border")
        
        self.player.deletePlayerRes()
    
