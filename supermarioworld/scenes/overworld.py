from supermarioworld.package_scenes import EmptyScene

from supermarioworld.tilemaps.tilemap import OverWorldMap



class OverWorld(EmptyScene):
    def __init__(self, game, biome: str, music_name: str, map_ref: str):
        super().__init__(game)

        # Audio
        self.audio.load(music_name)
        self.audio.setVolume(self.account.getMusicVolume())
        self.audio.play(loops=-1, fade_in=4)

        # Assets
        self.assets.pushAtlas("overworld", "overworld/overworld.png")
        self.assets.regImage("overworld-border", "overworld/overworld-border.png")

        self.overworld_map = OverWorldMap(game=game, biome=biome, atlas_key="overworld")
        self.overworld_map.load(map_ref)


    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        self.game.clearColor(0.53, 0.99, 1)

        self.RENDER.clearPrompt()

        self.overworld_map.submit(self.RENDER)
        #self.RENDER.submitSprite("overworld-border", size=(self.game.width, self.game.height))

        self.RENDER.renderSprite()
    

    def onSave(self):
        return super().onSave()
    
