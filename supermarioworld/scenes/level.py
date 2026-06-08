from supermarioworld.scenes.base import EmptyScene
from supermarioworld.tilemaps.level_tilemap import LevelTileMap



class Level(EmptyScene):
    def __init__(self, game, biome: str, music_name: str):
        super().__init__(game)

        self.audio.load(music_name)
        self.audio.play(loops=-1, fade_in=3)

        BASE_BIOME_CLEAR_COLOR = {
            0: (0.53, 0.99, 1),
            1: (0.227, 0.184, 0.388),
            2: (0.561, 0.02, 0.263),
            3: (0.549, 0, 0.212),
        }

        self.clear_color = BASE_BIOME_CLEAR_COLOR.get(biome, (0, 0, 0))

    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)


    def preRender(self):
        self.game.clearColor(self.clear_color[0], self.clear_color[1], self.clear_color[2])


    def postRender(self):
        pass
    

    def onRender(self):
        self.preRender()
        self.postRender()
    

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
    