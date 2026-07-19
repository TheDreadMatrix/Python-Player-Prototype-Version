from supermarioworld.typing.gametype import GameType, BasicEvent


class EmptyScene:
    
    def __init__(self, game: GameType, scene_name: str, **kwargs):
        self.game = game
        self.SCENE_NAME = scene_name

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


        # register begin
        self.assets.beginScene(self.SCENE_NAME)
        self.renderer.beginScene(self.SCENE_NAME)

        self.onInitialization(game, **kwargs)
        
    def onInitialization(self, game: GameType, **kwargs): pass

    

    def onUpdate(self): pass
    def onEvent(self, event: BasicEvent): pass
    def onRender(self): pass
    def onSave(self): pass