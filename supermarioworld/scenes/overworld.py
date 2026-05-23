from supermarioworld.package_scenes import EmptyScene

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


    def onUpdate(self):
        self.request.setTitle(f"{self.game.getFps():.2f}")
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        self.game.clearColor(0.53, 0.99, 1)

        self.RENDER.clearPrompt()

        self.overworld_map.submit(self.RENDER)
        self.RENDER.submitSprite("overworld-border", size=(self.game.width, self.game.height))

        self.RENDER.renderSprite()
    

    def onSave(self):
        return super().onSave()
    
