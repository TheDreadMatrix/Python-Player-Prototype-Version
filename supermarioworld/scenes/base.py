from supermarioworld.package_typing import GameType, Evalent


class EmptyScene:
    def __init__(self, game: "GameType"):
        self.game = game
        self.request = game.request
        self.paths = game.paths
        self.assets = game.assets
        self.audio = game.audio
        self.account = game.account

        self.locale = game.locale
        
        self.renderer = game.renderer

    def onUpdate(self): pass
    def onEvent(self, event: Evalent): pass
    def onRender(self): pass
    def onSave(self): pass