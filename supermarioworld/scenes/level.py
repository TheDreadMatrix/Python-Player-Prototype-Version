from supermarioworld.package_scenes import EmptyScene
from supermarioworld.tilemaps.level_tilemap import LevelTileMap



class Level(EmptyScene):
    def __init__(self, game, biome: str, music_name: str):
        super().__init__(game)

        self.audio.load(music_name)
        self.audio.setVolume(self.game.settings_read["music"])
        self.audio.play(loops=-1, fade_in=3)

    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        return super().onRender()
    

    def onSave(self):
        return super().onSave()




class Tutorial(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

    def onUpdate(self):
        return super().onUpdate()


    def onEvent(self, event):
        return super().onEvent(event)


    def onRender(self):
        return super().onRender()
    