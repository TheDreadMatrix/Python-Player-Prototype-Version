from supermarioworld.scenes.base import EmptyScene
from supermarioworld.tilemaps.level_tilemap import LevelTileMap



class Level(EmptyScene):
    def __init__(self, game, biome: int, music_name: str):
        super().__init__(game)

        self.audio.load(music_name)
        self.audio.play(loops=-1)

    

    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)


    
    

    def onRender(self):
        pass
    

    def onSave(self):
        return super().onSave()





    