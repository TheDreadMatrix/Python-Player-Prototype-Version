from supermarioworld.rendering.renderer import MainRenderer
from supermarioworld.package_typing import GameType

class EmptyScene:
    def __init__(self, game: "GameType"):
        self.game = game
        self.request = game.request
        self.paths = game.paths
        self.assets = game.assets
        self.audio = game.audio
        self.account = game.account
        
        self.RENDER = MainRenderer(game)

    def onUpdate(self): pass
    def onEvent(self, event): pass
    def onRender(self): pass
    def onSave(self): pass