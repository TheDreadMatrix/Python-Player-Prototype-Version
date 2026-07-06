from supermarioworld.typing.gametype import GameType
from supermarioworld.johnson import readData

from supermarioworld.rendering.animation import AnimationCutOut

from supermarioworld.tilemaps.spatial_hash import ChunkHasher, TileEntity
from supermarioworld.configuration import DRAW_TILE_SIZE, DRAW_BIGGER_TILE_SIZE, PIXEL_TILE_SIZE



class OverWorldMap:
    def __init__(self, game: GameType, notation_file: str, notation_file_buildings: str="overworld/notations/tile-notation-buildings.json"):
        self.game = game

        

        # Spatial
        self.spatial_hash = ChunkHasher(cell_sizes=(500, 450))

        # Some registration
        self.assets = game.assets
        self.renderer = game.renderer
        self.paths = game.paths
        
    

        notation_data = readData(self.paths.ConfigPath(notation_file))
        notation_building_data = readData(self.paths.ConfigPath(notation_file_buildings))

        self.notation = notation_data.get("tiles", {})
        self.notation_building = notation_building_data.get("tiles", {})
        
        game.assets.regAtlas("overworld", notation_data.get("img-ref", "overworld/overworld.png"))
        game.assets.regAtlas("overworld-buildings", notation_building_data.get("img-ref", "overworld/overworld.png"))

        self.map_data = {}
        self.buildings = {}

        self.building_layers = []
        self.layers = []

        self.tiles_build = []
        self.tiles = []
        self.tile_entities = {}
        
        self.animations: dict[str, AnimationCutOut] = {}

        self._registered_keys = set()



    def _load_map(self, map_name: str):
        path_map = f"overworld/maps/{map_name}.json"
        path_mapso = f"overworld/mapso/{map_name}.json"

        self.map_data = readData(self.paths.ConfigPath(path_map))
        self.buildings = readData(self.paths.ConfigPath(path_mapso))
        
        

    def _iter_tile_layers(self, dict_data: dict[str, list]):
        for key, value in dict_data.items():
            if key.startswith("tile-map-") and isinstance(value, list):
                return value
        return []
            
    def _get_texture_key(self, tile_key):
        if tile_key in self.animations:
            return self.animations[tile_key].getTextureKey()
        return tile_key

    def _get_raw_tile_key(self, tile_key: str):
        return tile_key.split(":", 1)
        

    @staticmethod
    def _is_empty_tile(tile_key) -> bool:
        return tile_key in (None, "", "0", 0, -1, "-1")

    def _normalize_tile_key(self, raw_tile, tile_type="map"):
        prefix = "map" if tile_type == "map" else "build"
        notation = self.notation if tile_type == "map" else self.notation_building
        
        if self._is_empty_tile(raw_tile):
            return None
        
        if isinstance(raw_tile, str):
            if raw_tile in notation:
                return f"{prefix}:{raw_tile}"
            
            if raw_tile.isdigit():
                key = f"t{raw_tile}"
                return key if key in notation else None
            return None
        return None

    def _register_used_tiles(self):
        # Register world map tiles
        used_keys = set()
       
        # Map tile
        for row in self.layers:
            for tile_key in row:
                normalized_key = self._normalize_tile_key(tile_key)
                if normalized_key is not None:
                    used_keys.add(normalized_key)

        # Build tile
        for tile_build_dict in self.building_layers:
            tile_type = tile_build_dict.get("type")
            if tile_type is None:
                continue
            normalized_key = self._normalize_tile_key(tile_build_dict["type"], tile_type="build")
            
            if normalized_key is not None:
                used_keys.add(normalized_key)

        

        for tile_key in used_keys:
            if tile_key in self._registered_keys:
                continue


            prefix, real_key = self._get_raw_tile_key(tile_key)
            
            
            tile = self.notation[real_key] if prefix == "map" else self.notation_building[real_key]
            atlas_key = "overworld" if prefix == "map" else "overworld-buildings"


            if isinstance(tile, dict) and "frames" in tile:
                # ANIMATION
                key_images = [f"{tile_key}_{i}" for i in range(len(tile["frames"]))]

                anim = AnimationCutOut(
                    game=self.game,
                    key_atlas=atlas_key,
                    frames=[(*f.get("xy", (0, 0)), *f.get("wh", (PIXEL_TILE_SIZE, PIXEL_TILE_SIZE))) for f in tile["frames"]],
                    durations=tile.get("durations", [0.1] * len(tile["frames"])),
                    key_images=key_images,
                )

                self.animations[tile_key] = anim

            else:
                if isinstance(tile, dict):
                    
                    x, y = tile.get("xy", (0, 0))
                    w, h = tile.get("wh", (PIXEL_TILE_SIZE, PIXEL_TILE_SIZE))
                else:
                    x = int(tile[0])
                    y = int(tile[1])
                    w, h = (PIXEL_TILE_SIZE, PIXEL_TILE_SIZE)

                self.assets.regCutOutImage("global", texture_key=tile_key, atlas_key=atlas_key, x=x, y=y, w=w, h=h)
                self._registered_keys.add(tile_key)

    def _build_entities(self):
        entities = []

        for tile_build_dict in self.building_layers:
            x, y = tile_build_dict.get("xy", (0, 0))
            tile_type = tile_build_dict.get("type")
            if tile_type is None:
                continue
            normalized_key = self._normalize_tile_key(tile_build_dict["type"], tile_type="build")

            self.tiles_build.append(TileEntity(tile=normalized_key, x=x, y=y, s_w=DRAW_BIGGER_TILE_SIZE, s_h=DRAW_BIGGER_TILE_SIZE, flx=0, fly=0))

        
        for row_i, row in enumerate(self.layers):
            
            for col_i, tile_key in enumerate(row):
                    

                normalized_key = self._normalize_tile_key(tile_key)

                if normalized_key is None:
                    continue

                _, real_key = self._get_raw_tile_key(normalized_key)
                tile = self.notation[real_key] 

                if isinstance(tile, list): 
                    flx, fly = (0, 0)
                else:
                    flx = tile.get("flx", 0)
                    fly = tile.get("fly", 0)

                tile_entity = TileEntity(tile=normalized_key, x=col_i * DRAW_TILE_SIZE, y=row_i * DRAW_TILE_SIZE, s_w=DRAW_TILE_SIZE, s_h=DRAW_TILE_SIZE, flx=flx, fly=fly)
                entities.append(tile_entity)
                
                self.tile_entities[(row_i, col_i)] = tile_entity
                
                
        
        
        self.spatial_hash.setEntities(entities)

    def load(self, map_ref):
        self._load_map(map_ref)

        self.layers = self._iter_tile_layers(self.map_data)
        self.building_layers = self._iter_tile_layers(self.buildings)
        

        self._register_used_tiles()

        self._build_entities()

        
    def set_tile(self, row: int, col: int, tile: str, sound=None):
        entity = self.tile_entities[(row, col)]
        entity.tile = self._normalize_tile_key(tile)
        
        if sound:
            sound.play()

    

    def update(self, player):
        cell = self.spatial_hash.getCellSizes(player.position[0], player.position[1])

        if cell != player.current_cells:
            self.tiles = self.spatial_hash.getEntities(player.position[0], player.position[1])
            player.current_cells = cell


        for animation in self.animations.values():
            animation.update()

    


    def renderMap(self, camera, r=1, g=1, b=1):
        batches = {}
        x, y = camera.apply(0, 0)

        for tile in self.tiles:
            tex = self._get_texture_key(tile.tile)
            batches.setdefault(tex, []).append([tile.x, tile.y, tile.s_w, tile.s_h, tile.flx, tile.fly])

        
        for texture_key, instances in batches.items():
            self.renderer.renderInstance(
                texture_key,
                position=(x, y), 
                instances=instances, r=r, g=g, b=b
            )

        for tile in self.tiles_build:
            tex = self._get_texture_key(tile.tile)
            self.renderer.render(tex, size=(tile.s_w, tile.s_h), position=(tile.x + x, tile.y + y), flx=tile.flx, fly=tile.fly)
    


   
