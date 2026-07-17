from supermarioworld.typing.gametype import GameType, BasicEvent


class EmptyScene:
    NAME = "BASE-ABC"
    def __init__(self, game: GameType, **kwargs):
        self.game = game

        self.settings = game.settings
        for name, value in vars(self.settings).items():
            setattr(self, name, value)

        self.request = game.request
        self.paths = game.paths
        self.assets = game.assets
        self.audio = game.audio
        self.account = game.account

        self.locale = game.locale
        
        self.renderer = game.renderer

        self.onInitialization(game, **kwargs)

    def onInitialization(self, game: GameType, **kwargs): pass

    

    def onUpdate(self): pass
    def onEvent(self, event: BasicEvent): pass
    def onRender(self): pass
    def onSave(self): pass