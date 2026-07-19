from supermarioworld.scenes.base import EmptyScene


class Settings(EmptyScene):
    def onInitialization(self, game, **kwargs):
        pass

    def onUpdate(self):
        pass
    
    def onEvent(self, event):
        pass
    
    def onRender(self):
        self.game.clearColor(0, 1, 0)
    
    def onSave(self):
        pass
