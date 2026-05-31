from supermarioworld.scenes.base import EmptyScene


class Settings(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

    def onUpdate(self):
        pass
    
    def onEvent(self, event):
        pass
    
    def onRender(self):
        self.game.clearColor(0, 1, 0)
    
    def onSave(self):
        pass
