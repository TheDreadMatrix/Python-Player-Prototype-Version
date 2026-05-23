from supermarioworld.package_scenes import EmptyScene
from supermarioworld.package_typing import GameType


class Settings(EmptyScene):
    def __init__(self, game: GameType):
        super().__init__(game)

    def onUpdate(self):
        pass
    
    def onEvent(self, event):
        pass
    
    def onRender(self):
        self.game._ctx.clear(0, 1, 0)
    
    def onSave(self):
        pass
