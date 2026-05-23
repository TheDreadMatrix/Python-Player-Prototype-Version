from supermarioworld.package_typing import GameType
from supermarioworld.package_scenes import EmptyScene

from supermarioworld.scenes.level import Level, Tutorial
from supermarioworld.scenes.overworld import OverWorld
from supermarioworld.scenes.menu import Menu, QuitScene
from supermarioworld.scenes.settings import Settings
from supermarioworld.scenes.cutscene import CutsceneScene

from supermarioworld.scenes.editor_overlevel import LevelEditor
from supermarioworld.scenes.editor_overworld import OverworldEditor

from supermarioworld.daenums import LevelBiome, OverWorldBiome, REDIRECT_TO_OVERWORLD




class SceneManager:
    def onLoad(self, game: GameType):
        game.assets.regMusic("title", "title-name.mp3")


        game.assets.regMusic("overworld-1", "overworld/valley-of-ones.mp3")
        game.assets.regMusic("overworld-4", "overworld/danger-zone-lava-land.mp3")

        game.assets.regMusic("A", "level/1.ogg")
        game.assets.regMusic("B", "level/2.ogg")
        game.assets.regMusic("CS", "level/3.ogg")

        game.assets.regSound("choose", "map.wav")
        game.assets.regSound("pause", "pause.wav")
        game.assets.regSound("pointer", "pointer.mp3")

    def __init__(self, game: GameType):
        self.game = game
        self.manager_state = ""
        self.current_scene = EmptyScene(game)


        self.game.request.redirectScene("overworld-1")


        self.scene_dict = {

            "overworld-editor-developer": lambda: EmptyScene(game=game),
            "level-editor-developer": lambda: EmptyScene(game=game),
            
            "level-editor": lambda: LevelEditor(game=game),
            "overworld-editor": lambda: OverworldEditor(game=game),


            #IN GAME
            "menu": lambda: Menu(game=game),
            "settings": lambda: Settings(game=game),
            "quit": lambda: QuitScene(game=game),

            "cutscene-1": lambda: CutsceneScene(game=game, cutscene_id="cutscene-1", redirect_scene=REDIRECT_TO_OVERWORLD),
            "ending": lambda: CutsceneScene(game=game, cutscene_id="ending", redirect_scene=REDIRECT_TO_OVERWORLD),

            "tutorial": lambda: Tutorial(game=game),

            "bonus-game-1": lambda: EmptyScene(game=game),
            "bonus-game-2": lambda: EmptyScene(game=game),
            
            
            "overworld-1": lambda: OverWorld(game=game, biome=OverWorldBiome.VALLEY, music_name="overworld-1", map_ref="overworld-1"),
            "overworld-2": lambda: OverWorld(game=game, biome=OverWorldBiome.UNDERGROUND, music_name="overworld-2", map_ref="overworld-2"),
            "overworld-3": lambda: OverWorld(game=game, biome=OverWorldBiome.RED_FOREST, music_name="overworld-3", map_ref="overworld-3"),
            "overworld-4": lambda: OverWorld(game=game, biome=OverWorldBiome.MAGMA, music_name="overworld-4", map_ref="overworld-4"),

            "overworld-star": lambda: OverWorld(game=game, biome=OverWorldBiome.SPECIAL, music_name="overworld-star", map_ref="overworld-star"),

            "level-1": lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"),
            "level-2": lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"),
            "level-3": lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"),
            "level-4": lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"),

            "level-5": lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B"),
            "level-6": lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A"),
            "level-7": lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B"),
            "level-8": lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A"),
            "level-9": lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"),

            "level-10": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-11": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-12": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"),
            "level-13": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"),
            "level-14": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-15": lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"),

            "level-16": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-17": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-18": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-19": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"),
            "level-20": lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"),

            "level-kaizo-1": lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"),
            "level-kaizo-2": lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A"),
            "level-kaizo-3": lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"),
            "level-kaizo-4": lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS")
        }

    

    def save(self):
        pass



    def update(self):
        state_scene = self.game.getScene()
            
        if state_scene != self.manager_state:
            self.current_scene.onSave()
            self.current_scene = self.scene_dict.get(state_scene)()
            self.manager_state = state_scene

        self.current_scene.onUpdate()


    def event(self, event):
        self.current_scene.onEvent(event)



    def render(self):
        self.current_scene.onRender()   
          

