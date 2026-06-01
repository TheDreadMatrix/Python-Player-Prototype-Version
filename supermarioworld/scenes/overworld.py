from supermarioworld.scenes.base import EmptyScene

from supermarioworld.tilemaps.overworld_tilemap import OverWorldMap
from supermarioworld.entities.overworld_entities import OverWorldPlayer

from supermarioworld.rendering.users import TextLabel, FadeLabel
from supermarioworld.rendering.camera import Camera

import pygame as pg


class OverWorld(EmptyScene):
    def __init__(self, game, biome: str, music_name: str, map_ref: str):
        super().__init__(game)

        # Camera
        self.camera = Camera(screen_width=game.width, screen_height=game.height, smooth=0.02)
        self.camera.setBounds(0, 0, 2500, 2500)

        # Audio
        self.audio.load(music_name)
        self.audio.setVolume(self.account.getMusicVolume())
        self.audio.play(loops=-1, fade_in=4)

        self.assets.regImage("overworld-border", "overworld/overworld-border.png")

        BASE_BIOME_DICT = {
            0: "tile-notation-valley",
            1: "tile-notation-underground",
            2: "tile-notation-red-forest",
            3: "tile-notation-magma",
            4: "tile-notation-special"
        }

        BASE_BIOME_CLEAR_COLOR = {
            0: (0.53, 0.99, 1),
            1: (0.227, 0.184, 0.388),
            2: (0.561, 0.02, 0.263),
            3: (0.549, 0, 0.212),
            4: (0, 0, 0)
        }

        self.r, self.g, self.b = BASE_BIOME_CLEAR_COLOR.get(biome, (0.53, 0.99, 1))



        self.overworld_map = OverWorldMap(game=game, notation_file=f"overworld/notations/{BASE_BIOME_DICT.get(biome)}.json")
        self.overworld_map.load(map_ref)

        self.player = OverWorldPlayer(game, map_ref=map_ref)

        self.text_titles = TextLabel(game, "titles", font_key="pixel", size_font=18)
        self.text_account = TextLabel(game, "text-account", f"#PS - {self.account.getCurrentPlayer().getSlot()}", font_key="pixel", size_font=18)
        self.text_points = TextLabel(game, "text-points", text="MOVING: 'WASD', SELECT: 'Q', EXIT TO MENU: 'E'", font_key="pixel", size_font=15)


        self.OUT_FADE = False
        self.fade_label = FadeLabel(game=game)
        self.fade_label.fadeIn(speed=1.5)
     


    def onUpdate(self):
        self.request.setTitle(f"{self.game.getFps():.2f}")

        self.overworld_map.update(self.player)
        self.camera.follow(self.player.position[0], self.player.position[1])

        self.fade_label.update()
        # Fade out effect
        if self.player.redirecting and not self.OUT_FADE:
            self.audio.fadeOut(2)
            self.fade_label.fadeOut(speed=1.5)
            self.OUT_FADE = True

        # If we coming to new node
        if self.text_titles.text != self.player._getTitleNode():
            self.text_titles.setText(self.player._getTitleNode())

        self.player.updatePlayer(self.game.delta_time)
    

    def onEvent(self, event):
        # for test
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.request.restartScene()

        self.player.handleEventNodes(event=event)
    

    def onRender(self):
        self.game.clearColor(self.r, self.g, self.b)

    
        self.overworld_map.renderMap(self.camera)

        self.player.renderPlayer(self.camera)

        self.renderer.render("overworld-border", size=(self.game.width, self.game.height))
        self.renderer.render(self.text_titles.texture_id, size=self.text_titles.size, position=(165, 70))
        self.renderer.render(self.text_account.texture_id, size=self.text_account.size, position=(600, 70))
        self.renderer.render(self.text_points.texture_id, size=self.text_points.size, position=(65, 495))

        self.fade_label.render()
    

    def onSave(self):
        self.overworld_map.delRes()
        self.assets.delImage("overworld-border")
        self.player.deletePlayerRes()
    
