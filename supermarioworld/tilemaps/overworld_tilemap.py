from supermarioworld.package_typing import GameType
from supermarioworld.johnson import readData

from supermarioworld.tilemaps.spatial_hash import ChunkHasher

from dataclasses import dataclass


@dataclass
class TileEntity:
    tile: str
    x: float
    y: float 
    s_w: float
    s_h: float
    flx: bool
    fly: bool



class OverWorldMap:
    def __init__(self, game: GameType, notation_file: str):
        # Spatial
        self.spatial_hash = ChunkHasher(cell_sizes=(500, 450))
        self.tiles = []

        # Some registration
        self.assets = game.assets
        self.renderer = game.renderer
        self.paths = game.paths

        self.atlas_key = "overworld"
        self.maps_dir = "overworld/maps"

        self.tile_size = 8
        self.draw_tile_size = 24
        

        notation_data = readData(self.paths.ConfigPath(notation_file))

        self.notation = notation_data["tiles"]
        
        game.assets.regAtlas("overworld", notation_data["img-ref"])

        self.map_data = {}
        self.layers = []
        
        self._registered_keys = set()



    def _load_map(self, map_name: str):
        path = f"{self.maps_dir}/{map_name}.json"
        self.map_data = readData(self.paths.ConfigPath(path))
        

    def _iter_tile_layers(self):
        for key, value in self.map_data.items():
            if key.startswith("tile-map-") and isinstance(value, list):
                yield value

    @staticmethod
    def _is_empty_tile(tile_key) -> bool:
        return tile_key in (None, "", "0", 0, -1, "-1")

    def _normalize_tile_key(self, raw_tile):
        if self._is_empty_tile(raw_tile):
            return None
        
        if isinstance(raw_tile, str):
            if raw_tile in self.notation:
                return raw_tile
            if raw_tile.isdigit():
                key = f"t{raw_tile}"
                return key if key in self.notation else None
            return None
        return None

    def _register_used_tiles(self):
        used_keys = set()
        for layer in self.layers:
            for row in layer:
                for tile_key in row:
                    normalized_key = self._normalize_tile_key(tile_key)
                    if normalized_key is not None:
                        used_keys.add(normalized_key)

       

        for tile_key in used_keys:
            if tile_key in self._registered_keys:
                continue
            tile_xy = self.notation[tile_key]
            x = int(tile_xy[0])
            y = int(tile_xy[1])
            self.assets.regCutOutImage(
                texture_key=tile_key,
                atlas_key=self.atlas_key,
                x=x,
                y=y,
                w=self.tile_size,
                h=self.tile_size,
            )
            self._registered_keys.add(tile_key)

    def _build_entities(self):
        entities = []

        for layer_index, layer in enumerate(self.layers, start=1):

            flx = layer_index > 1
            fly = layer_index > 1

            for row_i, row in enumerate(layer):
                for col_i, tile_key in enumerate(row):

                    normalized_key = self._normalize_tile_key(tile_key)

                    if normalized_key is None:
                        continue

                    entities.append(
                        TileEntity(
                            tile=normalized_key,
                            x=col_i * self.draw_tile_size,
                            y=row_i * self.draw_tile_size,
                            s_w=self.draw_tile_size,
                            s_h=self.draw_tile_size,
                            flx=flx,
                            fly=fly
                        )
                    )
        
        
        self.spatial_hash.setEntities(entities)

    def load(self, map_ref):
        self._load_map(map_ref)

        self.layers = list(self._iter_tile_layers())

        self._register_used_tiles()

        self._build_entities()

    

    def update(self, player):
        cell = self.spatial_hash.getCellSizes(player.position[0], player.position[1])

        if cell != player.current_cells:
            self.tiles = self.spatial_hash.getEntities(player.position[0], player.position[1])
            player.current_cells = cell

    


    def renderMap(self, camera, r=1, g=1, b=1):
        batches = {}
        x, y = camera.apply(0, 0)

        for tile in self.tiles:
            batches.setdefault(tile.tile, []).append([tile.x, tile.y, tile.s_w, tile.s_h, tile.flx, tile.fly])

        
        for texture_key, instances in batches.items():
            self.renderer.renderInstance(
                texture_key,
                position=(x, y), 
                instances=instances, r=r, g=g, b=b
            )
    


    def delRes(self):
        for tile_key in self._registered_keys:
            self.assets.delImage(tile_key)

        self.tiles.clear()
        self._registered_keys.clear()
        self.map_data.clear()
        self.layers.clear()

   
