from supermarioworld.scenes.base import EmptyScene

from supermarioworld.tilemaps.overworld_tilemap import OverWorldMap
from supermarioworld.entities.overworld_entities import OverWorldPlayer

from supermarioworld.rendering.users import TextLabel

import pygame as pg


class OverWorld(EmptyScene):
    def __init__(self, game, biome: str, music_name: str, map_ref: str):
        super().__init__(game)

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
        
        self._build_instance_batches()
        

    def _build_instance_batches(self):
        self._map_instance_batches = {}
        batches = {}
        for cmd in self.overworld_map.commands:
            batches.setdefault(cmd["texture"], []).append(  
                [cmd["position"][0], cmd["position"][1], cmd["size"][0], cmd["size"][1], 0.0, 0.0]
            )
        self._map_instance_batches = batches


    def onUpdate(self):
        self.request.setTitle(f"{self.game.getFps():.2f}")

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

        
        for texture_key, instances in self._map_instance_batches.items():
            self.renderer.renderInstance(texture_key, instances=instances)

        self.player.renderPlayer()

        self.renderer.render("overworld-border", size=(self.game.width, self.game.height))
        self.renderer.render(self.text_titles.texture_id, size=self.text_titles.size, position=(165, 70))
    

    def onSave(self):
        for texture_key, _ in self._map_instance_batches.items():
            self.assets.delImage(texture_key)
        self.assets.delImage("overworld-border")
        self.player.deletePlayerRes()
    
