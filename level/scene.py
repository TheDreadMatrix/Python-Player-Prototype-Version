from supermarioworld.scenes.base import EmptyScene
from supermarioworld.typing.gametype import GameType
from level.level_tilemap import LevelTileMap



class Level(EmptyScene):
    def onInitialization(self, game: GameType, biome: int, music_name: str):

        self.audio.load(music_name)
        self.audio.play()

    

    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)


    def onRender(self):
        self.renderer.renderQuad()
    

    def onSave(self):
        return super().onSave()





    