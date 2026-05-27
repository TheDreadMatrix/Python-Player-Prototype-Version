import json
from collections import defaultdict

import pygame as pg
import moderngl as mgl

from supermarioworld.scenes.base import EmptyScene
from supermarioworld.rendering.users import TextLabel
from supermarioworld.tilemaps.spatial_hash import SpatialHash


class OverworldEditor(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        self.assets.regAtlas("overworld", "overworld/overworld.png")

        self.audio.load("CS")
        self.audio.play(loops=-1)

        # game.paths.ConfigFolder("oveworld/maps")
        self.maps_dir = game.paths.ConfigFolder("overworld/maps")

        self.tile_size = 8
        self.cell_size = 32
        self.grid_origin = (20, 100)
        self.min_grid_cols = 50
        self.min_grid_rows = 50
        self.view_offset = [0, 0]
        self.zoom = 1.0
        self.zoom_min = 0.1
        self.zoom_max = 3.0
        self.palette_scroll_rows = 0
        self.palette_pos = [0, 120]
        self._drag_palette = False
        self._drag_palette_off = (0, 0)

        self.notation = self._load_json(game.paths.ConfigPath("overworld/notations/tile-notation-valley.json"))["tiles"]
        self.palette_keys = [k for k, v in self.notation.items() if isinstance(v, list) and len(v) >= 2]
        self.selected_tile = self.palette_keys[0] if self.palette_keys else None

        self.assets_to_release = set()
        self._register_palette_textures()
        self._register_ui_textures()

        # game.paths.findGlobal(self.maps_dir, file_category="*.json")
        self.map_files = sorted([p for p in game.paths.findGlobal(self.maps_dir, file_category="*.json")])
        self.map_index = 0

        self.map_path = None
        self.map_json = {}
        self.layer_keys = []
        self.layer_index = 0
        self.dirty = False
        self.status = "Ready"
        self.status_timer = 0.0
        self._prev_mouse_buttons = (False, False, False)
        self._prev_mouse_pos = pg.mouse.get_pos()
        self.undo_stack = []
        self._tile_hash = SpatialHash(16)
        self._tile_hash_dirty = True
        self._cached_map_batches = {}
        self._cached_grid_instances = []
        self._cached_palette_batches = {}
        self._cached_ui_batches = {"ow-ui-btn": [], "ow-ui-btn-hot": []}
        self._cached_label_batches = {}

        self._create_labels()
        self._load_current_map()

    def _create_labels(self):
        self.title_label = TextLabel(self.game, "ow-title", "OVERWORLD EDITOR", size_font=24)
        self.title_label.position = (20, 20)

        self.map_label = TextLabel(self.game, "ow-map", "", size_font=20)
        self.map_label.position = (20, 56)

        self.layer_label = TextLabel(self.game, "ow-layer", "", size_font=18)
        self.layer_label.position = (380, 56)

        self.tile_label = TextLabel(self.game, "ow-tile", "", size_font=18)
        self.tile_label.position = (20, 72)

        self.status_label = TextLabel(self.game, "ow-status", "", size_font=18)
        self.status_label.position = (20, self.game.height - 30)

    def _load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, path, data):
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
        self._register_solid_texture("ow-ui-tile-frame", (220, 40, 40, 255))
        self.assets_to_release.update({"ow-ui-btn", "ow-ui-btn-hot", "ow-ui-grid", "ow-ui-select", "ow-ui-tile-frame"})

    def _register_solid_texture(self, key: str, rgba: tuple[int, int, int, int]):
        surface = pg.Surface((1, 1), flags=pg.SRCALPHA)
        surface.fill(rgba)
        texture = self.renderer._ctx.texture(surface.get_size(), 4, pg.image.tobytes(surface, "RGBA"))
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.assets._regRawImage(key, texture)

    def _render_batch(self, texture_key: str, instances):
        if instances:
            self.renderer.renderInstance(texture_key, instances=instances)

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
        self.status = f"Loaded: {self.map_path}"
        self._tile_hash_dirty = True

    def _normalize_active_layer(self):
        if not self.layer_keys:
            self.map_json["tile-map-world"] = []
            self.layer_keys = ["tile-map-world"]
            self.layer_index = 0
        self.layer_index = max(0, min(self.layer_index, len(self.layer_keys) - 1))
        layer = self._active_layer()
        default_tile = "tile-1" if "tile-1" in self.notation else ""
        is_completely_empty = all((not cell) for row in layer for cell in row) if layer else True

        # Ensure every layer has enough editable space even if source JSON is tiny.
        while len(layer) < self.min_grid_rows:
            layer.append([])

        width = max((len(row) for row in layer), default=0)
        width = max(width, self.min_grid_cols)
        for row in layer:
            while len(row) < width:
                row.append(default_tile if is_completely_empty else "")

    def _active_layer_key(self):
        return self.layer_keys[self.layer_index]

    def _active_layer(self):
        return self.map_json[self._active_layer_key()]

    def _get_grid_size(self):
        layer = self._active_layer()
        rows = len(layer)
        cols = max((len(row) for row in layer), default=0)
        return cols, rows

    def _map_cell_size(self):
        return max(1, int(self.cell_size * self.zoom))

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
        self._tile_hash_dirty = True
        self._set_status(f"Layer: {self._active_layer_key()}")

    def _select_tile_delta(self, delta: int):
        if not self.palette_keys:
            return
        idx = self.palette_keys.index(self.selected_tile)
        idx = (idx + delta) % len(self.palette_keys)
        self.selected_tile = self.palette_keys[idx]

    def _paint(self, mouse_pos, erase: bool):
        cols, rows = self._get_grid_size()
        map_cell = self._map_cell_size()
        gx, gy = self.grid_origin
        mx, my = mouse_pos
        mx -= self.view_offset[0]
        my -= self.view_offset[1]
        tx = (mx - gx) // map_cell
        ty = (my - gy) // map_cell
        if tx < 0 or ty < 0 or tx >= cols or ty >= rows:
            return False

        layer = self._active_layer()
        current = layer[ty][tx]
        new_value = "" if erase else self.selected_tile
        if current == new_value:
            return False

        self.undo_stack.append((self._active_layer_key(), tx, ty, current))
        layer[ty][tx] = new_value
        self.dirty = True
        self._tile_hash_dirty = True
        return True

    def _undo_last(self):
        if not self.undo_stack:
            self._set_status("Nothing to undo")
            return

        layer_key, tx, ty, prev_value = self.undo_stack.pop()
        layer = self.map_json.get(layer_key)
        if not isinstance(layer, list) or ty < 0 or ty >= len(layer):
            self._set_status("Undo skipped")
            return
        row = layer[ty]
        if not isinstance(row, list) or tx < 0 or tx >= len(row):
            self._set_status("Undo skipped")
            return

        row[tx] = prev_value
        self.dirty = True
        self._tile_hash_dirty = True
        self._set_status("Undo")

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

    def _palette_rects(self):
        rects = []
        start_x, start_y, _, _ = self._palette_view_rect()
        per_row = self._palette_per_row()
        pad = 4
        row_offset = self.palette_scroll_rows * (self.cell_size + pad)
        for i, tile_key in enumerate(self.palette_keys):
            cx = i % per_row
            cy = i // per_row
            x = start_x + cx * (self.cell_size + pad)
            y = start_y + cy * (self.cell_size + pad) - row_offset
            rects.append((tile_key, (x, y, self.cell_size, self.cell_size)))
        return rects

    def _palette_per_row(self):
        return 14

    def _palette_view_rect(self):
        pad = 4
        per_row = self._palette_per_row()
        width = per_row * self.cell_size + (per_row - 1) * pad
        if self.palette_pos[0] == 0:
            self.palette_pos[0] = self.game.width - width - 20
        x = max(0, min(self.game.width - width, self.palette_pos[0]))
        top = max(0, min(self.game.height - self.cell_size, self.palette_pos[1]))
        self.palette_pos[0], self.palette_pos[1] = x, top
        bottom = self.game.height - 60
        height = max(self.cell_size, bottom - top)
        return (x, top, width, height)

    def _palette_max_scroll_rows(self):
        per_row = self._palette_per_row()
        total_rows = (len(self.palette_keys) + per_row - 1) // per_row
        _, _, _, view_h = self._palette_view_rect()
        pad = 4
        visible_rows = max(1, (view_h + pad) // (self.cell_size + pad))
        return max(0, total_rows - visible_rows)

    def _scroll_palette(self, delta_rows: int):
        max_rows = self._palette_max_scroll_rows()
        self.palette_scroll_rows = max(0, min(max_rows, self.palette_scroll_rows + delta_rows))

    def _over_ui(self, pos):
        for rect in self._ui_rects().values():
            if self._in_rect(pos, rect):
                return True
        return False

    def _over_palette(self, pos):
        if self._in_rect(pos, self._palette_view_rect()):
            return True
        for _, rect in self._palette_rects():
            if self._in_rect(pos, rect):
                return True
        return False

    def _save_current_map(self):
        if self.map_path is None:
            self._set_status("No map file to save")
            return
        self._save_json(self.map_path, self.map_json)
        self.dirty = False
        self._set_status(f"Saved: {self.map_path}")

    def onUpdate(self):
        self.request.setTitle(f"{self.game.getFps():.2f}")
        if self.status_timer > 0:
            self.status_timer -= self.game.delta_time
        else:
            self.status = ""

        self._handle_mouse_input()

        self.map_label.setText(f"Map: {'Map' if self.map_path else 'none'} {'*' if self.dirty else ''}")
        self.layer_label.setText(f"Layer: {self._active_layer_key() if self.layer_keys else 'none'}")
        self.tile_label.setText(f"Tile: {self.selected_tile if self.selected_tile else 'none'}")
        self.status_label.setText(self.status if self.status else "LMB draw | RMB erase | MMB pan | Wheel zoom | [/] map | ;/' layer | Q/E tile | Ctrl+S save")
        self._rebuild_render_cache()

    def _rebuild_render_cache(self):
        self._cached_map_batches = self._build_map_batches()
        self._cached_grid_instances = self._build_grid_instances()
        self._cached_palette_batches = self._build_palette_batches()
        self._cached_ui_batches = self._build_ui_batches()
        self._cached_label_batches = self._build_label_batches()

    def _handle_mouse_input(self):
        mouse_pos = pg.mouse.get_pos()
        left, middle, right = pg.mouse.get_pressed(3)
        prev_left, prev_middle, prev_right = self._prev_mouse_buttons
        rects = self._ui_rects()
        palette_rect = self._palette_view_rect()

        if left and not prev_left and self._in_rect(mouse_pos, palette_rect):
            picked = self._pick_tile_from_palette(mouse_pos)
            if not picked:
                self._drag_palette = True
                self._drag_palette_off = (mouse_pos[0] - self.palette_pos[0], mouse_pos[1] - self.palette_pos[1])

        if not left:
            self._drag_palette = False

        if self._drag_palette:
            self.palette_pos[0] = mouse_pos[0] - self._drag_palette_off[0]
            self.palette_pos[1] = mouse_pos[1] - self._drag_palette_off[1]
            self._prev_mouse_buttons = (left, middle, right)
            self._prev_mouse_pos = mouse_pos
            return

        over_ui = self._over_ui(mouse_pos)
        over_palette = self._over_palette(mouse_pos)

        if middle:
            dx = mouse_pos[0] - self._prev_mouse_pos[0]
            dy = mouse_pos[1] - self._prev_mouse_pos[1]
            self.view_offset[0] += dx
            self.view_offset[1] += dy
            if not prev_middle:
                self._set_status("Pan map")

        # UI buttons should trigger once per click, not every frame while held.
        if left and not prev_left:
            if over_ui and self._in_rect(mouse_pos, rects["save"]):
                self._save_current_map()
                self._prev_mouse_buttons = (left, middle, right)
                self._prev_mouse_pos = mouse_pos
                return
            if over_ui and self._in_rect(mouse_pos, rects["prev_map"]):
                self._switch_map(-1)
                self._prev_mouse_buttons = (left, middle, right)
                self._prev_mouse_pos = mouse_pos
                return
            if over_ui and self._in_rect(mouse_pos, rects["next_map"]):
                self._switch_map(1)
                self._prev_mouse_buttons = (left, middle, right)
                self._prev_mouse_pos = mouse_pos
                return
            if over_ui and self._in_rect(mouse_pos, rects["prev_layer"]):
                self._switch_layer(-1)
                self._prev_mouse_buttons = (left, middle, right)
                self._prev_mouse_pos = mouse_pos
                return
            if over_ui and self._in_rect(mouse_pos, rects["next_layer"]):
                self._switch_layer(1)
                self._prev_mouse_buttons = (left, middle, right)
                self._prev_mouse_pos = mouse_pos
                return

        if left and not middle and not over_ui and not over_palette:
            if self._paint(mouse_pos, erase=False):
                self._set_status("Draw")

        if right and not middle and not over_ui and not over_palette and self._paint(mouse_pos, erase=True):
            self._set_status("Erase")

        self._prev_mouse_buttons = (left, middle, right)
        self._prev_mouse_pos = mouse_pos

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
            elif event.key == pg.K_z and (event.mod & pg.KMOD_CTRL):
                self._undo_last()
            elif event.key in (pg.K_EQUALS, pg.K_PLUS, pg.K_KP_PLUS):
                self._change_zoom(0.1)
            elif event.key in (pg.K_MINUS, pg.K_KP_MINUS):
                self._change_zoom(-0.1)
        elif event.type == pg.MOUSEWHEEL:
            mouse_pos = pg.mouse.get_pos()
            if self._in_rect(mouse_pos, self._palette_view_rect()):
                self._scroll_palette(-event.y)
            else:
                self._change_zoom(0.1 if event.y > 0 else -0.1)

    def _change_zoom(self, delta: float):
        old_zoom = self.zoom
        self.zoom = max(self.zoom_min, min(self.zoom_max, self.zoom + delta))
        if self.zoom != old_zoom:
            self._set_status(f"Zoom: {self.zoom:.1f}x")

    def _pick_tile_from_palette(self, pos):
        if not self._in_rect(pos, self._palette_view_rect()):
            return False
        for tile_key, rect in self._palette_rects():
            if self._in_rect(pos, rect):
                self.selected_tile = tile_key
                self._set_status(f"Selected {tile_key}")
                return True
        return False

    def onRender(self):
        self.game.clearColor(0.12, 0.2, 0.3)
        self._render_from_cache()

    def _render_from_cache(self):
        for texture_key, instances in self._cached_map_batches.items():
            self._render_batch(texture_key, instances)
        self._render_batch("ow-ui-grid", self._cached_grid_instances)
        for texture_key, instances in self._cached_palette_batches.items():
            self._render_batch(texture_key, instances)
        for texture_key, instances in self._cached_ui_batches.items():
            self._render_batch(texture_key, instances)
        for texture_key, instances in self._cached_label_batches.items():
            self._render_batch(texture_key, instances)

    def _build_map_batches(self):
        map_batches = defaultdict(list)
        if not self.layer_keys:
            return map_batches
        map_cell = self._map_cell_size()
        screen_w, screen_h = self.game.width, self.game.height
        gx, gy = self.grid_origin
        ox, oy = self.view_offset
        layer = self._active_layer()
        if self._tile_hash_dirty:
            entities = []
            for y, row in enumerate(layer):
                for x, tile_key in enumerate(row):
                    if tile_key and tile_key in self.notation:
                        entities.append({"x": x, "y": y, "tile_key": tile_key})
            self._tile_hash.setEntities(entities)
            self._tile_hash_dirty = False
        cx = ((screen_w / 2) - gx - ox) / map_cell
        cy = ((screen_h / 2) - gy - oy) / map_cell
        rx = (screen_w / 2) / map_cell + 2
        ry = (screen_h / 2) / map_cell + 2
        for e in self._tile_hash.getEntities(cx, cy, rx, ry):
            px = gx + e["x"] * map_cell + ox
            py = gy + e["y"] * map_cell + oy
            if px + map_cell <= 0 or px >= screen_w or py + map_cell <= 0 or py >= screen_h:
                continue
            map_batches[e["tile_key"]].append([px, py, map_cell, map_cell, 0.0, 0.0])
        return map_batches

    def _build_grid_instances(self):
        cols, rows = self._get_grid_size()
        if cols == 0 or rows == 0:
            return []
        map_cell = self._map_cell_size()
        screen_w, screen_h = self.game.width, self.game.height
        gx, gy = self.grid_origin
        ox, oy = self.view_offset
        w = cols * map_cell
        h = rows * map_cell
        grid_instances = []
        for ix in range(cols + 1):
            px = gx + ix * map_cell + ox
            py = gy + oy
            if px < 0 or px >= screen_w:
                continue
            if py + h <= 0 or py >= screen_h:
                continue
            draw_y = max(py, 0)
            draw_h = min(py + h, screen_h) - draw_y
            if draw_h > 0:
                grid_instances.append([px, draw_y, 1, draw_h, 0.0, 0.0])
        for iy in range(rows + 1):
            px = gx + ox
            py = gy + iy * map_cell + oy
            if py < 0 or py >= screen_h:
                continue
            if px + w <= 0 or px >= screen_w:
                continue
            draw_x = max(px, 0)
            draw_w = min(px + w, screen_w) - draw_x
            if draw_w > 0:
                grid_instances.append([draw_x, py, draw_w, 1, 0.0, 0.0])
        return grid_instances

    def _build_palette_batches(self):
        batches = defaultdict(list)
        view_x, view_y, view_w, view_h = self._palette_view_rect()
        batches["ow-ui-btn"].append([view_x, view_y, view_w, view_h, 0.0, 0.0])
        for tile_key, rect in self._palette_rects():
            x, y, _, _ = rect
            if y + self.cell_size <= view_y or y >= view_y + view_h:
                continue
            batches[tile_key].append([x, y, self.cell_size, self.cell_size, 0.0, 0.0])
            # Red frame around each tile button in palette.
            batches["ow-ui-tile-frame"].append([x, y, self.cell_size, 1, 0.0, 0.0])
            batches["ow-ui-tile-frame"].append([x, y + self.cell_size - 1, self.cell_size, 1, 0.0, 0.0])
            batches["ow-ui-tile-frame"].append([x, y, 1, self.cell_size, 0.0, 0.0])
            batches["ow-ui-tile-frame"].append([x + self.cell_size - 1, y, 1, self.cell_size, 0.0, 0.0])
            if tile_key == self.selected_tile:
                batches["ow-ui-select"].append([x, y + self.cell_size - 2, self.cell_size, 2, 0.0, 0.0])
        return batches

    def _build_ui_batches(self):
        rects = self._ui_rects()
        mouse_pos = pg.mouse.get_pos()
        batches = {"ow-ui-btn": [], "ow-ui-btn-hot": []}
        for key, rect in rects.items():
            base = "ow-ui-btn-hot" if self._in_rect(mouse_pos, rect) else "ow-ui-btn"
            target = batches["ow-ui-btn-hot"] if base == "ow-ui-btn-hot" else batches["ow-ui-btn"]
            target.append([rect[0], rect[1], rect[2], rect[3], 0.0, 0.0])
        return batches

    def _build_label_batches(self):
        batches = defaultdict(list)
        batches[self.title_label.texture_id].append([self.title_label.position[0], self.title_label.position[1], self.title_label.size[0], self.title_label.size[1], 0.0, 0.0])
        batches[self.map_label.texture_id].append([self.map_label.position[0], self.map_label.position[1], self.map_label.size[0], self.map_label.size[1], 0.0, 0.0])
        batches[self.layer_label.texture_id].append([self.layer_label.position[0], self.layer_label.position[1], self.layer_label.size[0], self.layer_label.size[1], 0.0, 0.0])
        batches[self.tile_label.texture_id].append([self.tile_label.position[0], self.tile_label.position[1], self.tile_label.size[0], self.tile_label.size[1], 0.0, 0.0])
        batches[self.status_label.texture_id].append([self.status_label.position[0], self.status_label.position[1], self.status_label.size[0], self.status_label.size[1], 0.0, 0.0])

        for text, pos in [("Save", (676, 22)), ("<", (652, 58)), (">", (758, 58)), ("<", (652, 92)), (">", (758, 92))]:
            key, size = self._resolve_button_text_texture(text, pos)
            batches[key].append([pos[0], pos[1], size[0], size[1], 0.0, 0.0])
        return batches

    def _resolve_button_text_texture(self, text: str, pos: tuple[int, int]):
        key = f"ow-btn-{text}-{pos[0]}-{pos[1]}"
        if key not in self.assets.textures:
            label = TextLabel(self.game, self.renderer, key, text, size_font=20)
            self.assets_to_release.add(key)
            self.assets_to_release.add(label.texture_id)
            return label.texture_id, label.size
        return key, (22, 24)

    def onSave(self):
        for key in self.assets_to_release:
            if key in self.assets.textures:
                self.assets.delImage(key)
