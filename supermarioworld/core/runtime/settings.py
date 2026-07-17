import importlib




class Settings:
    def __init__(self, PROJECT_NAME):
        module = importlib.import_module(f"{PROJECT_NAME}.settings")
        
        for name, value in vars(module).items():
            if not name.startswith("__"):
                setattr(self, name, value)

        assets = importlib.import_module(f"{PROJECT_NAME}.assets")
        scenes = importlib.import_module(f"{PROJECT_NAME}.scenes")

        self.ATLASES = assets.ATLASES
        self.FONTS = assets.FONTS
        self.MUSIC = assets.MUSIC
        self.SOUNDS = assets.SOUNDS

        self.SAVE_CALLBACK = scenes.SAVE_CALLBACK
        self.START_SCENE = scenes.START_SCENE
        self.SCENES = scenes.SCENES