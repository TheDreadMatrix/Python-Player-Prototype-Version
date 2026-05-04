from supermarioworld.package_typing import EmptyScene, GameType


from supermarioworld.scenes.levels import Level, Tutorial
from supermarioworld.scenes.overworld import OverWorld
from supermarioworld.scenes.menu import Menu, Settings
from supermarioworld.scenes.cutscene import CutsceneScene
from supermarioworld.scenes.editor_overlevel import LevelEditor
from supermarioworld.scenes.editor_overworld import OverworldEditor



class SceneManager:
    def __init__(self, game: GameType):
        self.game = game
        self.manager_state = ""
        self.current_scene = EmptyScene(game)


        self.game.request.redirectScene("menu")


        self.scene_dict = {
            
            "level-editor": lambda: LevelEditor(game=game),
            "overworld-editor": lambda: OverworldEditor(game=game),


            #IN GAME
            "menu": lambda: Menu(game=game),
            "settings": lambda: Settings(game=game),
            "quit": lambda: EmptyScene(game=game),

            "tutorial": lambda: Tutorial(game=game),
            "cutscene-1": lambda: CutsceneScene(game=game),

            "bonus-game-1": lambda: EmptyScene(game=game),
            "bonus-game-2": lambda: EmptyScene(game=game),
            
            "ending": lambda: EmptyScene(game=game),

            "overworld-1": lambda: OverWorld(game=game, biome="valley", music_name="overworld-1"),
            "overworld-2": lambda: OverWorld(game=game, biome="cave", music_name="overworld-2"),
            "overworld-3": lambda: OverWorld(game=game, biome="tropic", music_name="overworld-3"),
            "overworld-4": lambda: OverWorld(game=game, biome="magma", music_name="overworld-4"),
            "overworld-star": lambda: OverWorld(game=game, biome="star", music_name="overworld-star"),

            "level-1": lambda: Level(game=game, biome="valley", music_name="world-A"),
            "level-2": lambda: Level(game=game, biome="valley", music_name="world-A"),
            "level-3": lambda: Level(game=game, biome="valley", music_name="atletic-A"),
            "level-4": lambda: Level(game=game, biome="castle", music_name="castle"),

            "level-5": lambda: Level(game=game, biome="cave", music_name="underground-B"),
            "level-6": lambda: Level(game=game, biome="cave", music_name="underground-A"),
            "level-7": lambda: Level(game=game, biome="cave", music_name="underground-B"),
            "level-8": lambda: Level(game=game, biome="cave", music_name="underground-A"),
            "level-9": lambda: Level(game=game, biome="castle", music_name="castle"),

            "level-10": lambda: Level(game=game, biome="valley", music_name="world-B"),
            "level-11": lambda: Level(game=game, biome="valley", music_name="atletic-B"),
            "level-12": lambda: Level(game=game, biome="forest", music_name="world-A"),
            "level-13": lambda: Level(game=game, biome="forest", music_name="world-A"),
            "level-14": lambda: Level(game=game, biome="valley", music_name="atletic-B"),
            "level-15": lambda: Level(game=game, biome="castle", music_name="castle"),

            "level-16": lambda: Level(game=game, biome="magma", music_name="castle-B"),
            "level-17": lambda: Level(game=game, biome="magma", music_name="castle-B"),
            "level-18": lambda: Level(game=game, biome="magma", music_name="castle-B"),
            "level-19": lambda: Level(game=game, biome="magma", music_name="castle-B"),
            "level-20": lambda: Level(game=game, biome="castle", music_name="castle"),

            "level-kaizo-1": lambda: Level(game=game, biome="valley", music_name="world-A"),
            "level-kaizo-2": lambda: Level(game=game, biome="cave", music_name="underground-A"),
            "level-kaizo-3": lambda: Level(game=game, biome="forest", music_name="atletic-A"),
            "level-kaizo-4": lambda: Level(game=game, biome="magma", music_name="castle-B")
        }

    

    def save(self):
        pass



    def update(self):
        state_scene = self.game.getScene()

        if state_scene == "quit":
            self.game.request.closeGame()
            
        if state_scene != self.manager_state:
            self.current_scene.onSave()
            self.current_scene = self.scene_dict.get(state_scene)()
            self.manager_state = state_scene

        self.current_scene.onUpdate()


    def event(self, event):
        self.current_scene.onEvent(event)



    def render(self):
        self.current_scene.onRender()        

