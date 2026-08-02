from supermarioworld.typing.gametype import GameType
from supermarioworld.johnson import readData



"""
block-1: {"xywh": [], "class": "Block"}


load-map
give-objects
"""

class LevelTileMap:
    def __init__(self, game: GameType, notation_file: str):
        self.game = game

        self.assets = game.assets
        self.renderer = game.renderer
        self.paths = game.paths


        