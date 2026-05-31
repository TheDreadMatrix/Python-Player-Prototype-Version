from supermarioworld.core.router import SceneManager

from supermarioworld.scenes.base import EmptyScene


from supermarioworld.scenes.level import Level, Tutorial
from supermarioworld.scenes.overworld import OverWorld
from supermarioworld.scenes.menu import Menu, QuitScene
from supermarioworld.scenes.settings import Settings
from supermarioworld.scenes.cutscene import CutsceneScene

from supermarioworld.scenes.editor_overlevel import LevelEditor
from supermarioworld.scenes.editor_overworld import OverworldEditor

from supermarioworld.daenums import LevelBiome, OverWorldBiome, REDIRECT_TO_OVERWORLD


class Bootloader(SceneManager):
    def onLoad(self, game):
        # Fonts
        game.assets.regFont("pixel", "PixelFont.ttf")

        # Musics
        game.assets.regMusic("title", "title-name.mp3")


        game.assets.regMusic("overworld-1", "overworld/valley-of-ones.mp3")
        game.assets.regMusic("overworld-4", "overworld/danger-zone-lava-land.mp3")

        game.assets.regMusic("A", "level/1.ogg")
        game.assets.regMusic("B", "level/2.ogg")
        game.assets.regMusic("CS", "level/3.ogg")


        # Sounds
        game.assets.regSound("cancel", "cancel.wav")
        game.assets.regSound("choose", "map.wav")
        game.assets.regSound("pause", "pause.wav")
        game.assets.regSound("pointer", "pointer.mp3")

        game.assets.regSound("losing", "lost.mp3")
        game.assets.regSound("success", "success.mp3")

        game.assets.regSound("coin", "coins.mp3")
        game.assets.regSound("jumping", "jump.mp3")
        game.assets.regSound("scroll", "scroll.wav")

        
        

    def onInitScene(self, game):
        self.START_SCENE = "base:overworld-1"

        self.registerScene("base:level-editor", lambda: LevelEditor(game=game))
        self.registerScene("base:overworld-editor", lambda: OverworldEditor(game=game))

        self.registerScene("base:menu", lambda: Menu(game=game))
        self.registerScene("base:settings", lambda: Settings(game=game))
        self.registerScene("base:quit", lambda: QuitScene(game=game))
        
        self.registerScene("base:cutscene-1", lambda: CutsceneScene(game=game, cutscene_id="cutscene-1", redirect_scene=REDIRECT_TO_OVERWORLD))
        self.registerScene("base:ending", lambda: CutsceneScene(game=game, cutscene_id="ending", redirect_scene=REDIRECT_TO_OVERWORLD))

        self.registerScene("base:tutorial", lambda: Tutorial(game=game))
        self.registerScene("base:bonus-game-1", lambda: EmptyScene(game=game))
        self.registerScene("base:bonus-game-2", lambda: EmptyScene(game=game))

        self.registerScene("base:overworld-1", lambda: OverWorld(game=game, biome=OverWorldBiome.VALLEY, music_name="overworld-1", map_ref="overworld-1"))
        self.registerScene("base:overworld-2", lambda: OverWorld(game=game, biome=OverWorldBiome.UNDERGROUND, music_name="overworld-4", map_ref="overworld-2"))
        self.registerScene("base:overworld-3", lambda: OverWorld(game=game, biome=OverWorldBiome.RED_FOREST, music_name="overworld-4", map_ref="overworld-3"))
        self.registerScene("base:overworld-4", lambda: OverWorld(game=game, biome=OverWorldBiome.MAGMA, music_name="overworld-4", map_ref="overworld-4"))
        self.registerScene("base:overworld-star", lambda: OverWorld(game=game, biome=OverWorldBiome.SPECIAL, music_name="overworld-star", map_ref="overworld-star"))

        self.registerScene("base:level-1", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))
        self.registerScene("base:level-2", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="B"))
        self.registerScene("base:level-3", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))
        self.registerScene("base:level-4", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"))
        self.registerScene("base:level-5", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B"))
        self.registerScene("base:level-6", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A"))
        self.registerScene("base:level-7", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B"))
        self.registerScene("base:level-8", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A"))
        self.registerScene("base:level-9", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"))

        self.registerScene("base:level-10", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-11", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-12", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:level-13", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:level-14", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-15", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"))

        self.registerScene("base:level-16", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-17", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-18", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-19", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-20", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"))

        self.registerScene("base:level-kaizo-1", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))
        self.registerScene("base:level-kaizo-2", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A"))
        self.registerScene("base:level-kaizo-3", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:level-kaizo-4", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS"))
