import json


class OverWorldMap:
    def __init__(self, game, biome: str, atlas_key: str = "overworld", notation_file: str = "overworld/tile-notation.json",
        maps_dir: str = "overworld/maps"):
        
        self.assets = game.assets
        self.paths = game.paths

        self.biome = biome
        self.atlas_key = atlas_key
        self.notation_file = notation_file
        self.maps_dir = maps_dir

        self.tile_size = 8
        self.draw_tile_size = 32
        self.notation = self._load_json(self.notation_file)
        self.map_data = {}
        self.layers = []
        self.commands = []
        self._registered_keys = set()

    def _load_json(self, relative_config_path: str):
        cfg_path = self.paths.ConfigPath(relative_config_path)
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _resolve_map_name(self, map_ref: str | int | None = None) -> str:
        if map_ref is None:
            return self.biome
        if isinstance(map_ref, int):
            return f"overworld-{map_ref}"
        return map_ref

    def _load_map(self, map_name: str):
        path = f"{self.maps_dir}/{map_name}.json"
        self.map_data = self._load_json(path)

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

    def _build_commands(self):
        commands = []
        for layer_index, layer in enumerate(self.layers, start=1):
            for row_i, row in enumerate(layer):
                for col_i, tile_key in enumerate(row):
                    normalized_key = self._normalize_tile_key(tile_key)
                    if normalized_key is None:
                        continue
                    commands.append(
                        {
                            "texture": normalized_key,
                            "position": (col_i * self.draw_tile_size, row_i * self.draw_tile_size),
                            "size": (self.draw_tile_size, self.draw_tile_size),
                            "layer": layer_index,
                        }
                    )
        self.commands = commands

    def load(self, map_ref: str | int | None = None):
        map_name = self._resolve_map_name(map_ref)
        self._load_map(map_name)
        self.layers = list(self._iter_tile_layers())
        self._register_used_tiles()
        self._build_commands()
        return self.commands

    def submit(self, renderer):
        for cmd in self.commands:
            renderer.submitSprite(
                cmd["texture"],
                size=cmd["size"],
                position=cmd["position"],
                layer=cmd["layer"],
            )
