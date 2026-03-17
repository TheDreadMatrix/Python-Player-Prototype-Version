
from MyGame.anotation import GameType
    

class EmptyScene:
    def __init__(self, game: "GameType"):
        self.game = game

    def onUpdate(self): pass
    def onEvent(self, event): pass
    def onRender(self): pass
    def onSave(self): pass