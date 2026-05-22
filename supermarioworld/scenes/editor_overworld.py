from pathlib import Path
import json

import pygame as pg
import moderngl as mgl

from supermarioworld.package_scenes import EmptyScene
from supermarioworld.rendering.easygui import TextLabel


class OverworldEditor(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        self.assets.pushAtlas("overworld", "overworld/overworld.png")

        self.config_root = Path(self.paths.ConfigPath("overworld/tile-notation.json")).parent
        self.maps_dir = self.config_root / "maps"

        self.tile_size = 8
        self.cell_size = 32
        self.grid_origin = (20, 100)

        self.notation = self._load_json(self.config_root / "tile-notation.json")
        self.palette_keys = [k for k, v in self.notation.items() if isinstance(v, list) and len(v) >= 2]
        self.selected_tile = self.palette_keys[0] if self.palette_keys else None

        self.assets_to_release = set()
        self._register_palette_textures()
        self._register_ui_textures()

        self.map_files = sorted([p for p in self.maps_dir.glob("*.json") if p.is_file()])
        self.map_index = 0

        self.map_path = None
        self.map_json = {}
        self.layer_keys = []
        self.layer_index = 0
        self.dirty = False
        self.status = "Ready"
        self.status_timer = 0.0

        self._create_labels()
        self._load_current_map()

    def _create_labels(self):
        self.title_label = TextLabel(self.game, self.RENDER, "ow-title", "OVERWORLD EDITOR", size_font=24)
        self.title_label.position = (20, 20)

        self.map_label = TextLabel(self.game, self.RENDER, "ow-map", "", size_font=20)
        self.map_label.position = (20, 56)

        self.layer_label = TextLabel(self.game, self.RENDER, "ow-layer", "", size_font=18)
        self.layer_label.position = (380, 56)

        self.tile_label = TextLabel(self.game, self.RENDER, "ow-tile", "", size_font=18)
        self.tile_label.position = (20, 72)

        self.status_label = TextLabel(self.game, self.RENDER, "ow-status", "", size_font=18)
        self.status_label.position = (20, self.game.height - 30)

    def _load_json(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, path: Path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _register_palette_textures(self):
        for tile_key in self.palette_keys:
            x, y = self.notation[tile_key][:2]
            self.assets.regCutOutImage(tile_key, "overworld", int(x), int(y), self.tile_size, self.tile_size)
            self.assets_to_release.add(tile_key)

    def _register_ui_textures(self):
        self._register_solid_texture("ow-ui-btn", (60, 70, 88, 230))
        self._register_solid_texture("ow-ui-btn-hot", (85, 105, 135, 255))
        self._register_solid_texture("ow-ui-grid", (255, 255, 255, 100))
        self._register_solid_texture("ow-ui-select", (255, 235, 90, 220))
        self.assets_to_release.update({"ow-ui-btn", "ow-ui-btn-hot", "ow-ui-grid", "ow-ui-select"})

    def _register_solid_texture(self, key: str, rgba: tuple[int, int, int, int]):
        surface = pg.Surface((1, 1), flags=pg.SRCALPHA)
        surface.fill(rgba)
        texture = self.game._ctx.texture(surface.get_size(), 4, pg.image.tobytes(surface, "RGBA"))
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.assets._regRawImage(key, texture)

    def _load_current_map(self):
        if not self.map_files:
            self.map_path = None
            self.map_json = {}
            self.layer_keys = []
            self.layer_index = 0
            return

        self.map_path = self.map_files[self.map_index]
        self.map_json = self._load_json(self.map_path)
        self.layer_keys = [k for k, v in self.map_json.items() if k.startswith("tile-map-") and isinstance(v, list)]
        self.layer_index = 0
        self._normalize_active_layer()
        self.dirty = False
        self.status = f"Loaded: {self.map_path.stem}"

    def _normalize_active_layer(self):
        if not self.layer_keys:
            self.map_json["tile-map-world"] = []
            self.layer_keys = ["tile-map-world"]
            self.layer_index = 0
        self.layer_index = max(0, min(self.layer_index, len(self.layer_keys) - 1))
        layer = self._active_layer()
        width = max((len(row) for row in layer), default=0)
        for row in layer:
            while len(row) < width:
                row.append("")

    def _active_layer_key(self):
        return self.layer_keys[self.layer_index]

    def _active_layer(self):
        return self.map_json[self._active_layer_key()]

    def _get_grid_size(self):
        layer = self._active_layer()
        rows = len(layer)
        cols = max((len(row) for row in layer), default=0)
        return cols, rows

    def _set_status(self, text: str):
        self.status = text
        self.status_timer = 3.0

    def _switch_map(self, delta: int):
        if not self.map_files:
            return
        self.map_index = (self.map_index + delta) % len(self.map_files)
        self._load_current_map()

    def _switch_layer(self, delta: int):
        if not self.layer_keys:
            return
        self.layer_index = (self.layer_index + delta) % len(self.layer_keys)
        self._normalize_active_layer()
        self._set_status(f"Layer: {self._active_layer_key()}")

    def _select_tile_delta(self, delta: int):
        if not self.palette_keys:
            return
        idx = self.palette_keys.index(self.selected_tile)
        idx = (idx + delta) % len(self.palette_keys)
        self.selected_tile = self.palette_keys[idx]

    def _paint(self, mouse_pos, erase: bool):
        cols, rows = self._get_grid_size()
        gx, gy = self.grid_origin
        mx, my = mouse_pos
        tx = (mx - gx) // self.cell_size
        ty = (my - gy) // self.cell_size
        if tx < 0 or ty < 0 or tx >= cols or ty >= rows:
            return False

        layer = self._active_layer()
        current = layer[ty][tx]
        new_value = "" if erase else self.selected_tile
        if current == new_value:
            return False

        layer[ty][tx] = new_value
        self.dirty = True
        return True

    @staticmethod
    def _in_rect(pos, rect):
        x, y = pos
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh

    def _ui_rects(self):
        return {
            "save": (640, 16, 140, 34),
            "prev_map": (640, 56, 34, 28),
            "next_map": (746, 56, 34, 28),
            "prev_layer": (640, 90, 34, 28),
            "next_layer": (746, 90, 34, 28),
        }

    def _save_current_map(self):
        if self.map_path is None:
            self._set_status("No map file to save")
            return
        self._save_json(self.map_path, self.map_json)
        self.dirty = False
        self._set_status(f"Saved: {self.map_path.name}")

    def onUpdate(self):
        if self.status_timer > 0:
            self.status_timer -= self.game.delta_time
        else:
            self.status = ""

        self.map_label.setText(f"Map: {self.map_path.name if self.map_path else 'none'} {'*' if self.dirty else ''}")
        self.layer_label.setText(f"Layer: {self._active_layer_key() if self.layer_keys else 'none'}")
        self.tile_label.setText(f"Tile: {self.selected_tile if self.selected_tile else 'none'}")
        self.status_label.setText(self.status if self.status else "LMB draw | RMB erase | [/] map | ;/' layer | Q/E tile | Ctrl+S save")

    def onEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFTBRACKET:
                self._switch_map(-1)
            elif event.key == pg.K_RIGHTBRACKET:
                self._switch_map(1)
            elif event.key == pg.K_SEMICOLON:
                self._switch_layer(-1)
            elif event.key == pg.K_QUOTE:
                self._switch_layer(1)
            elif event.key == pg.K_q:
                self._select_tile_delta(-1)
            elif event.key == pg.K_e:
                self._select_tile_delta(1)
            elif event.key == pg.K_s and (event.mod & pg.KMOD_CTRL):
                self._save_current_map()

        if event.type == pg.MOUSEBUTTONDOWN:
            rects = self._ui_rects()
            if event.button == 1:
                if self._in_rect(event.pos, rects["save"]):
                    self._save_current_map()
                    return
                if self._in_rect(event.pos, rects["prev_map"]):
                    self._switch_map(-1)
                    return
                if self._in_rect(event.pos, rects["next_map"]):
                    self._switch_map(1)
                    return
                if self._in_rect(event.pos, rects["prev_layer"]):
                    self._switch_layer(-1)
                    return
                if self._in_rect(event.pos, rects["next_layer"]):
                    self._switch_layer(1)
                    return

                if self._paint(event.pos, erase=False):
                    self._set_status("Draw")
                    return

                self._pick_tile_from_palette(event.pos)

            elif event.button == 3 and self._paint(event.pos, erase=True):
                self._set_status("Erase")

    def _pick_tile_from_palette(self, pos):
        start_x = 20
        start_y = self.game.height - 160
        per_row = 14
        pad = 4
        for i, tile_key in enumerate(self.palette_keys):
            cx = i % per_row
            cy = i // per_row
            x = start_x + cx * (self.cell_size + pad)
            y = start_y + cy * (self.cell_size + pad)
            rect = (x, y, self.cell_size, self.cell_size)
            if self._in_rect(pos, rect):
                self.selected_tile = tile_key
                self._set_status(f"Selected {tile_key}")
                return

    def onRender(self):
        self.game.clearColor(0.12, 0.2, 0.3)
        self.RENDER.clearPrompt()

        self._render_map()
        self._render_grid()
        self._render_palette()
        self._render_ui()
        self._render_labels()

        self.RENDER.renderSprite()

    def _render_map(self):
        if not self.layer_keys:
            return
        gx, gy = self.grid_origin
        layer = self._active_layer()
        for y, row in enumerate(layer):
            for x, tile_key in enumerate(row):
                if not tile_key or tile_key not in self.notation:
                    continue
                self.RENDER.submitSprite(
                    tile_key,
                    size=(self.cell_size, self.cell_size),
                    position=(gx + x * self.cell_size, gy + y * self.cell_size),
                    layer=1,
                )

    def _render_grid(self):
        cols, rows = self._get_grid_size()
        if cols == 0 or rows == 0:
            return
        gx, gy = self.grid_origin
        w = cols * self.cell_size
        h = rows * self.cell_size
        for ix in range(cols + 1):
            self.RENDER.submitSprite("ow-ui-grid", size=(1, h), position=(gx + ix * self.cell_size, gy), layer=2)
        for iy in range(rows + 1):
            self.RENDER.submitSprite("ow-ui-grid", size=(w, 1), position=(gx, gy + iy * self.cell_size), layer=2)

    def _render_palette(self):
        start_x = 20
        start_y = self.game.height - 160
        per_row = 14
        pad = 4
        for i, tile_key in enumerate(self.palette_keys):
            cx = i % per_row
            cy = i // per_row
            x = start_x + cx * (self.cell_size + pad)
            y = start_y + cy * (self.cell_size + pad)
            self.RENDER.submitSprite(tile_key, size=(self.cell_size, self.cell_size), position=(x, y), layer=3)
            if tile_key == self.selected_tile:
                self.RENDER.submitSprite("ow-ui-select", size=(self.cell_size, 2), position=(x, y + self.cell_size - 2), layer=4)

    def _render_ui(self):
        rects = self._ui_rects()
        mouse_pos = pg.mouse.get_pos()
        for key, rect in rects.items():
            base = "ow-ui-btn-hot" if self._in_rect(mouse_pos, rect) else "ow-ui-btn"
            self.RENDER.submitSprite(base, size=(rect[2], rect[3]), position=(rect[0], rect[1]), layer=5)

    def _render_labels(self):
        self.RENDER.submitSprite(self.title_label.texture_id, size=self.title_label.size, position=self.title_label.position, layer=6)
        self.RENDER.submitSprite(self.map_label.texture_id, size=self.map_label.size, position=self.map_label.position, layer=6)
        self.RENDER.submitSprite(self.layer_label.texture_id, size=self.layer_label.size, position=self.layer_label.position, layer=6)
        self.RENDER.submitSprite(self.tile_label.texture_id, size=self.tile_label.size, position=self.tile_label.position, layer=6)
        self.RENDER.submitSprite(self.status_label.texture_id, size=self.status_label.size, position=self.status_label.position, layer=6)

        self._render_button_text("Save", (676, 22))
        self._render_button_text("<", (652, 58))
        self._render_button_text(">", (758, 58))
        self._render_button_text("<", (652, 92))
        self._render_button_text(">", (758, 92))

    def _render_button_text(self, text: str, pos: tuple[int, int]):
        key = f"ow-btn-{text}-{pos[0]}-{pos[1]}"
        if key not in self.assets.textures:
            label = TextLabel(self.game, self.RENDER, key, text, size_font=20)
            self.assets_to_release.add(key)
            self.assets_to_release.add(label.texture_id)
            self.RENDER.submitSprite(label.texture_id, size=label.size, position=pos, layer=6)
            return
        self.RENDER.submitSprite(key, size=(22, 24), position=pos, layer=6)

    def onSave(self):
        for key in self.assets_to_release:
            if key in self.assets.textures:
                self.assets.delImage(key)
