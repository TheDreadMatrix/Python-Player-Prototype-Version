from editor_level.scene import LevelEditor
from editor_overworld.scene import OverworldEditor
from level.scene import Level
from menu.scene import Menu, QuitScene
from overworld.scene import Overworld
from settings.scene import Settings


from supermarioworld.enums.game import LevelBiome, OverWorldBiome




START_SCENE = "base:level-7"
SAVE_CALLBACK = lambda: print("SAVED")


SCENES = {
    # Editors
    "base:level-editor": {
        "class": LevelEditor,
        "kwargs": {}
    },
    "base:overworld-editor": {
        "class": OverworldEditor,
        "kwargs": {}
    },

    # Menu
    "base:menu": {
        "class": Menu,
        "kwargs": {}
    },
    "base:settings": {
        "class": Settings,
        "kwargs": {}
    },
    "base:quit": {
        "class": QuitScene,
        "kwargs": {}
    },

    # Tutorial
    "base:tutorial": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.VALLEY,
            "music_name": "A",
        },
    },

    # Bonus
    "base:bonus-game-1": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "overworld-star",
        },
    },
    "base:bonus-game-2": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "overworld-star",
        },
    },

    # Overworld
    "base:overworld-1": {
        "class": Overworld,
        "kwargs": {
            "music_name": "overworld-1",
            "map_ref": "overworld-1",
            "biome": OverWorldBiome.VALLEY,
        },
    },
    "base:overworld-2": {
        "class": Overworld,
        "kwargs": {
            "music_name": "B-underground",
            "map_ref": "overworld-2",
            "biome": OverWorldBiome.UNDERGROUND,
        },
    },
    "base:overworld-3": {
        "class": Overworld,
        "kwargs": {
            "music_name": "overworld-3",
            "map_ref": "overworld-3",
            "biome": OverWorldBiome.RED_FOREST,
        },
    },
    "base:overworld-4": {
        "class": Overworld,
        "kwargs": {
            "music_name": "overworld-4",
            "map_ref": "overworld-4",
            "biome": OverWorldBiome.MAGMA,
        },
    },
    "base:overworld-star": {
        "class": Overworld,
        "kwargs": {
            "music_name": "overworld-star",
            "map_ref": "overworld-star",
            "biome": OverWorldBiome.SPECIAL,
        },
    },

    # Valley
    "base:level-1": {"class": Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "A"}},
    "base:level-2": {"class": Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "B"}},
    "base:level-3": {"class": Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "A"}},
    "base:level-4": {"class": Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "B"}},

    "base:ampliy-castle": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Underground
    "base:level-5": {"class": Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "B-underground"}},
    "base:level-6": {"class": Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "A-underground"}},
    "base:level-7": {"class": Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "B-underground"}},
    "base:level-8": {"class": Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "A-underground"}},
    "base:level-9": {"class": Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "B-underground"}},

    "base:fortress-1": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Red Forest
    "base:level-10": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-11": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-12": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},
    "base:level-13": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},
    "base:level-14": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-15": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},

    "base:raysky-castle": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Lavaland
    "base:level-16": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-17": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-18": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-19": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-20": {"class": Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},

    "base:lex-ultraman-castle": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Special
    "base:level-kaizo-1": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.VALLEY,
            "music_name": "A",
        },
    },
    "base:level-kaizo-2": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.UNDERGROUND,
            "music_name": "B-underground",
        },
    },
    "base:level-kaizo-3": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.RED_FOREST,
            "music_name": "B",
        },
    },
    "base:level-kaizo-4": {
        "class": Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },
}