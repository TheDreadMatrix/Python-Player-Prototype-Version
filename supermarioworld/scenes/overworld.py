from supermarioworld.scenes.base import EmptyScene

from supermarioworld.tilemaps.overworld_tilemap import OverWorldMap



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


        self.overworld_map = OverWorldMap(game=game, notation_file=f"overworld/notations/{BASE_BIOME_DICT.get(biome)}.json")
        self.overworld_map.load(map_ref)
        self._map_instance_batches = {}
        self._build_instance_batches()

    def _build_instance_batches(self):
        batches = {}
        for cmd in self.overworld_map.commands:
            batches.setdefault(cmd["texture"], []).append(
                [cmd["position"][0], cmd["position"][1], cmd["size"][0], cmd["size"][1], 0.0, 0.0]
            )
        self._map_instance_batches = batches


    def onUpdate(self):
        self.request.setTitle(f"{self.game.getFps():.2f}")
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        self.game.clearColor(0.53, 0.99, 1)

        
        for texture_key, instances in self._map_instance_batches.items():
            self.renderer.renderInstance(texture_key, instances=instances)

        self.renderer.render("overworld-border", size=(self.game.width, self.game.height))
    

    def onSave(self):
        return super().onSave()
    
