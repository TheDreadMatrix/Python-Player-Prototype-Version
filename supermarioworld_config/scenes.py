from supermarioworld.scenes import (
    menu,
    settings,
    overworld,
    level,
    editor_level,
    editor_overworld,
)

from supermarioworld.enums.game import LevelBiome, OverWorldBiome

def CALLBACK():
    print("SAVED")


START_SCENE = "base:overworld-1"
SAVE_CALLBACK = CALLBACK


SCENES = {
    # Editors
    "base:level-editor": {
        "class": editor_level.LevelEditor,
        "kwargs": {}
    },
    "base:overworld-editor": {
        "class": editor_overworld.OverworldEditor,
        "kwargs": {}
    },

    # Menu
    "base:menu": {
        "class": menu.Menu,
        "kwargs": {}
    },
    "base:settings": {
        "class": settings.Settings,
        "kwargs": {}
    },
    "base:quit": {
        "class": menu.QuitScene,
        "kwargs": {}
    },

    # Tutorial
    "base:tutorial": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.VALLEY,
            "music_name": "A",
        },
    },

    # Bonus
    "base:bonus-game-1": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "overworld-star",
        },
    },
    "base:bonus-game-2": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "overworld-star",
        },
    },

    # Overworld
    "base:overworld-1": {
        "class": overworld.Overworld,
        "kwargs": {
            "music_name": "overworld-1",
            "map_ref": "overworld-1",
            "biome": OverWorldBiome.VALLEY,
        },
    },
    "base:overworld-2": {
        "class": overworld.Overworld,
        "kwargs": {
            "music_name": "B-underground",
            "map_ref": "overworld-2",
            "biome": OverWorldBiome.UNDERGROUND,
        },
    },
    "base:overworld-3": {
        "class": overworld.Overworld,
        "kwargs": {
            "music_name": "overworld-3",
            "map_ref": "overworld-3",
            "biome": OverWorldBiome.RED_FOREST,
        },
    },
    "base:overworld-4": {
        "class": overworld.Overworld,
        "kwargs": {
            "music_name": "overworld-4",
            "map_ref": "overworld-4",
            "biome": OverWorldBiome.MAGMA,
        },
    },
    "base:overworld-star": {
        "class": overworld.Overworld,
        "kwargs": {
            "music_name": "overworld-star",
            "map_ref": "overworld-star",
            "biome": OverWorldBiome.SPECIAL,
        },
    },

    # Valley
    "base:level-1": {"class": level.Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "A"}},
    "base:level-2": {"class": level.Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "B"}},
    "base:level-3": {"class": level.Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "A"}},
    "base:level-4": {"class": level.Level, "kwargs": {"biome": LevelBiome.VALLEY, "music_name": "B"}},

    "base:ampliy-castle": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Underground
    "base:level-5": {"class": level.Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "B-underground"}},
    "base:level-6": {"class": level.Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "A-underground"}},
    "base:level-7": {"class": level.Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "B-underground"}},
    "base:level-8": {"class": level.Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "A-underground"}},
    "base:level-9": {"class": level.Level, "kwargs": {"biome": LevelBiome.UNDERGROUND, "music_name": "B-underground"}},

    "base:fortress-1": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Red Forest
    "base:level-10": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-11": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-12": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},
    "base:level-13": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},
    "base:level-14": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-15": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},

    "base:raysky-castle": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Lavaland
    "base:level-16": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-17": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-18": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-19": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "B"}},
    "base:level-20": {"class": level.Level, "kwargs": {"biome": LevelBiome.RED_FOREST, "music_name": "A"}},

    "base:lex-ultraman-castle": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },

    # Special
    "base:level-kaizo-1": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.VALLEY,
            "music_name": "A",
        },
    },
    "base:level-kaizo-2": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.UNDERGROUND,
            "music_name": "B-underground",
        },
    },
    "base:level-kaizo-3": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.RED_FOREST,
            "music_name": "B",
        },
    },
    "base:level-kaizo-4": {
        "class": level.Level,
        "kwargs": {
            "biome": LevelBiome.CASTLE,
            "music_name": "CS-A",
        },
    },
}