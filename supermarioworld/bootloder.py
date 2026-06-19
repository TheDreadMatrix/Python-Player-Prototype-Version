from supermarioworld.core.router import SceneManager


from supermarioworld.scenes.level import Level
from supermarioworld.scenes.overworld import OverWorld
from supermarioworld.scenes.menu import Menu, QuitScene
from supermarioworld.scenes.settings import Settings

from supermarioworld.scenes.editor_overlevel import LevelEditor
from supermarioworld.scenes.editor_overworld import OverworldEditor

from supermarioworld.enums.gameplay import OverWorldBiome, LevelBiome



class Bootloader(SceneManager):
    def onLoad(self, game):
        # Fonts and atlas
        game.assets.regAtlas("fonts", "atlas/fonts.png")
        game.assets.regFont("pixel", "PixelFont.ttf")

        # Musics
        game.assets.regMusic("title", "title-name.mp3")


        game.assets.regMusic("overworld-1", "overworld/valley-of-ones.ogg")
        game.assets.regMusic("overworld-2", "overworld/underground.ogg")
        game.assets.regMusic("overworld-3", "overworld/red-forest.ogg")
        game.assets.regMusic("overworld-4", "overworld/danger-zone-lava-land.mp3")
        game.assets.regMusic("overworld-star", "overworld/special-star.ogg")

        game.assets.regMusic("A", "level/A.ogg")
        game.assets.regMusic("B", "level/B.ogg")

        game.assets.regMusic("A-underground", "level/A-underground.ogg")
        game.assets.regMusic("B-underground", "level/B-underground.ogg")

        game.assets.regMusic("CS-A", "level/CS-A.ogg")
        game.assets.regMusic("CS-B", "level/CS-b.ogg")


        # Sounds
        game.assets.regSound("cancel", "wav/cancel.wav")
        game.assets.regSound("choose", "wav/map.wav")
        game.assets.regSound("pause", "wav/pause.wav")
        game.assets.regSound("scroll", "wav/scroll.wav")
        game.assets.regSound("thunder", "wav/smw_thunder.wav")

        game.assets.regSound("pointer", "mp3/pointer.mp3")
        game.assets.regSound("losing", "mp3/lost.mp3")
        game.assets.regSound("success", "mp3/success.mp3")

        game.assets.regSound("coin", "mp3/coins.mp3")
        game.assets.regSound("jumping", "mp3/jump.mp3")
        
      
        

    def onInitScene(self, game):
        self.START_SCENE = "base:overworld-1"

        # Developer
        self.registerScene("base:level-editor", lambda: LevelEditor(game=game))
        self.registerScene("base:overworld-editor", lambda: OverworldEditor(game=game, biome=OverWorldBiome.VALLEY, index_map=1))

        # First place scenes
        self.registerScene("base:menu", lambda: Menu(game=game))
        self.registerScene("base:settings", lambda: Settings(game=game))
        self.registerScene("base:quit", lambda: QuitScene(game=game))

    
        
    
        # Tutorial and bonus levels
        self.registerScene("base:tutorial", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))

        self.registerScene("base:bonus-game-1", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="overworld-star"))
        self.registerScene("base:bonus-game-2", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="overworld-star"))

        # Overworld
        self.registerScene("base:overworld-1", lambda: OverWorld(game=game, biome=OverWorldBiome.VALLEY, music_name="overworld-1", map_ref="overworld-1"))
        self.registerScene("base:overworld-2", lambda: OverWorld(game=game, biome=OverWorldBiome.UNDERGROUND, music_name="B-underground", map_ref="overworld-2"))
        self.registerScene("base:overworld-3", lambda: OverWorld(game=game, biome=OverWorldBiome.RED_FOREST, music_name="overworld-3", map_ref="overworld-3"))
        self.registerScene("base:overworld-4", lambda: OverWorld(game=game, biome=OverWorldBiome.MAGMA, music_name="overworld-4", map_ref="overworld-4"))
        self.registerScene("base:overworld-star", lambda: OverWorld(game=game, biome=OverWorldBiome.SPECIAL, music_name="overworld-star", map_ref="overworld-star"))

        # Valley of ones
        self.registerScene("base:level-1", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))
        self.registerScene("base:level-2", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="B"))
        self.registerScene("base:level-3", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))
        self.registerScene("base:level-4", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="B"))
        self.registerScene("base:ampliy-castle", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS-A"))

        # Crystal caves
        self.registerScene("base:level-5", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B-underground"))
        self.registerScene("base:level-6", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A-underground"))
        self.registerScene("base:level-7", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B-underground"))
        self.registerScene("base:level-8", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="A-underground"))
        self.registerScene("base:level-9", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B-underground"))
        self.registerScene("base:fortress-1", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS-A"))

        # Red forest
        self.registerScene("base:level-10", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-11", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-12", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:level-13", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:level-14", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-15", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:raysky-castle", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS-A"))

        # Danger zone lavaland
        self.registerScene("base:level-16", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-17", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-18", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-19", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-20", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="A"))
        self.registerScene("base:lex-ultraman-castle", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS-A"))

        # Special star
        self.registerScene("base:level-kaizo-1", lambda: Level(game=game, biome=LevelBiome.VALLEY, music_name="A"))
        self.registerScene("base:level-kaizo-2", lambda: Level(game=game, biome=LevelBiome.UNDERGROUND, music_name="B-underground"))
        self.registerScene("base:level-kaizo-3", lambda: Level(game=game, biome=LevelBiome.RED_FOREST, music_name="B"))
        self.registerScene("base:level-kaizo-4", lambda: Level(game=game, biome=LevelBiome.CASTLE, music_name="CS-A"))

        