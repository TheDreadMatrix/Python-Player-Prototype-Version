from collections import defaultdict

import pygame as pg

from supermarioworld.johnson import readData, saveData
from supermarioworld.package_typing import GameType
from supermarioworld.scenes.base import EmptyScene

from supermarioworld.rendering.users import TextLabel

from supermarioworld.enums.render import RenderMode

from supermarioworld.configuration import (NOTATION_BIOME_OVERWORLD, 
                                           PALETTE_PER_ROW, OVERWORLD_EDITOR_COLS, OVERWORLD_EDITOR_ROWS, MIN_ZOOM_EDITOR, MAX_ZOOM_EDITOR)



class OverworldEditor(EmptyScene):
    def __init__(self, game: GameType, biome: int=0):
        super().__init__(game)

        self.audio.load("CS-B")
        self.audio.play(loops=-1, fade_in=2000)



        self.tile_size = 8
        self.cell_size = 32
        self.grid_origin = (20, 100)

        self.view_offset = [0, 0]
        self.zoom = 1.0
  

        self.palette_scroll_rows = 0

        self.palette_pos = [0, 120]
        self._drag_palette = False
        self._drag_palette_off = (0, 0)

        # Read file and atlas

        notation = readData(game.paths.ConfigPath(f"overworld/notations/{NOTATION_BIOME_OVERWORLD.get(biome)}.json"))

        self.notation = notation["tiles"]
        self.assets.regAtlas("overworld", notation["img-ref"])


        self.palette_keys = [k for k, v in self.notation.items() if isinstance(v, list) and len(v) >= 2]
        self.selected_tile = self.palette_keys[0] if self.palette_keys else None

        self.assets_to_release = set()

        # Create texture and text
        self._register_palette_textures()
        self._create_labels()
        

        # Connect other files
        maps_dir = game.paths.ConfigFolder("overworld/maps")
        self.map_files = game.paths.findGlobal(maps_dir, file_category="*.json")
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

        self._cached_map_batches = {}

        self._selected_rect = None
    
    
        self._load_current_map()

    def _create_labels(self):
        self.title_label = TextLabel(self.game, "ow-title", "OVERWORLD EDITOR", font_key="pixel", size_font=24)
        self.title_label.position = (20, 20)

        self.map_label = TextLabel(self.game, "ow-map", "", size_font=20, font_key="pixel")
        self.map_label.position = (20, 56)

        self.layer_label = TextLabel(self.game, "ow-layer", "", size_font=18, font_key="pixel")
        self.layer_label.position = (380, 56)

        self.tile_label = TextLabel(self.game, "ow-tile", "", size_font=18, font_key="pixel")
        self.tile_label.position = (20, 72)

        self.status_label = TextLabel(self.game, "ow-status", "", size_font=15, font_key="pixel")
        self.status_label.position = (20, self.game.height - 30)

    def _register_palette_textures(self):
        for tile_key in self.palette_keys:
            x, y = self.notation[tile_key][:2]
            self.assets.regCutOutImage(tile_key, "overworld", int(x), int(y), self.tile_size, self.tile_size)
            self.assets_to_release.add(tile_key)



    def _load_current_map(self):
        if not self.map_files:
            self.map_path = None
            self.map_json = {}
            self.layer_keys = []
            self.layer_index = 0
            return

        self.map_path = self.map_files[self.map_index]
        self.map_json = readData(self.map_path)
        self.layer_keys = [k for k, v in self.map_json.items() if k.startswith("tile-map-") and isinstance(v, list)]
        self.layer_index = 0
        self._normalize_active_layer()
        self.dirty = False
        self.status = f"Loaded: {self.map_path}"
    

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
        while len(layer) < OVERWORLD_EDITOR_ROWS:
            layer.append([])

        width = max((len(row) for row in layer), default=0)
        width = max(width, OVERWORLD_EDITOR_COLS)
        for row in layer:
            while len(row) < width:
                row.append(default_tile if is_completely_empty else "")

    def _active_layer_key(self):
        return self.layer_keys[self.layer_index]

    def _active_layer(self):
        return self.map_json[self._active_layer_key()]


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
        layer = self._active_layer()
        rows = len(layer)
        cols = max((len(row) for row in layer), default=0)

        map_cell = max(1, int(self.cell_size * self.zoom))
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
        per_row = PALETTE_PER_ROW
        pad = 4
        row_offset = self.palette_scroll_rows * (self.cell_size + pad)
        for i, tile_key in enumerate(self.palette_keys):
            cx = i % per_row
            cy = i // per_row
            x = start_x + cx * (self.cell_size + pad)
            y = start_y + cy * (self.cell_size + pad) - row_offset
            rects.append((tile_key, (x, y, self.cell_size, self.cell_size)))
        return rects

    

    def _palette_view_rect(self):
        pad = 4
        per_row = PALETTE_PER_ROW
        width = per_row * self.cell_size + (per_row - 1) * pad
        if self.palette_pos[0] == 0:
            self.palette_pos[0] = self.game.width - width - 20
        x = max(-1, min(self.game.width - width, self.palette_pos[0]))
        top = max(0, min(self.game.height - self.cell_size, self.palette_pos[1]))
        self.palette_pos[0], self.palette_pos[1] = x, top
        bottom = self.game.height
        height = max(self.cell_size, bottom - top)
        return (x, top, width, height)

    def _palette_max_scroll_rows(self):
        per_row = PALETTE_PER_ROW
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
        saveData(self.map_path, self.map_json)
        self.dirty = False
        self._set_status(f"Saved: {self.map_path}")

    def onUpdate(self):
        self.request.setTitle(f"{self.game.getFps():.2f}")

        if self.status_timer > 0:
            self.status_timer -= self.game.delta_time
        else:
            self.status = ""

        self._handle_mouse_input()

        self.map_label.setText(f"Map: {"Some map" if self.map_path else 'none'} {'*' if self.dirty else ''}")
        self.layer_label.setText(f"Layer: {self._active_layer_key() if self.layer_keys else 'none'}")
        self.tile_label.setText(f"Tile: {self.selected_tile if self.selected_tile else 'none'}")
        self.status_label.setText(self.status if self.status else "LMB draw | RMB erase | MMB pan | Wheel zoom | [/] map | ;/' layer | Q/E tile | Ctrl+S save")
        


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
        self.zoom = max(MIN_ZOOM_EDITOR, min(MAX_ZOOM_EDITOR, self.zoom + delta))
        if self.zoom != old_zoom:
            self._set_status(f"Zoom: {self.zoom:.1f}x")

    def _pick_tile_from_palette(self, pos):
        if not self._in_rect(pos, self._palette_view_rect()):
            return False
        for tile_key, rect in self._palette_rects():
            if self._in_rect(pos, rect):
                self.selected_tile = tile_key
                return True
        return False

    def onRender(self):
        self._cached_map_batches = self._build_map_batches()
        

        self.game.clearColor(0.12, 0.2, 0.3)

        for texture_key, instances in self._cached_map_batches.items():
            self.renderer.renderInstance(texture_key, instances=instances)

        
        view_x, view_y, view_w, view_h = self._palette_view_rect()

        self.renderer.renderQuad(position=(view_x, view_y), size=(view_w, view_h), r=0.5, g=0.5, b=0.5, a=0.7)

        for tile_key, rect in self._palette_rects():
            x, y, _, _ = rect
            if y + self.cell_size <= view_y or y >= view_y + view_h:
                continue

            self.renderer.render(tile_key, position=(x, y), size=(self.cell_size, self.cell_size))
            

            if self.selected_tile == tile_key:
                self._selected_rect = rect
            

        if self._selected_rect:
            x, y, w, h = self._selected_rect
            self.renderer.renderQuad(position=(x, y), size=(w, h), r=1.0, g=0.0, b=0.0, a=1.0, mode=RenderMode.LINE_LOOP)

               

        

        self.renderer.renderQuad(position=(640, 16), size=(140, 34), a=0.7)
        self.renderer.renderQuad(position=(640, 56), size=(34, 28), a=0.7)
        self.renderer.renderQuad(position=(746, 56), size=(34, 28), a=0.7)
        self.renderer.renderQuad(position=(640, 90), size=(34, 28), a=0.7)
        self.renderer.renderQuad(position=(746, 90), size=(34, 28), a=0.7)

        self.title_label.render()
        self.map_label.render()
        self.tile_label.render()
        self.status_label.render()
        self.layer_label.render()

        
       
        
            

    def _build_map_batches(self):
        map_batches = defaultdict(list)

        if not self.layer_keys:
            return map_batches

        map_cell = max(1, int(self.cell_size * self.zoom))
        screen_w, screen_h = self.game.width, self.game.height
        gx, gy = self.grid_origin
        ox, oy = self.view_offset

        layer = self._active_layer()

    
        inv_cell = 1.0 / map_cell

        left   = int((-gx - ox) * inv_cell)
        top    = int((-gy - oy) * inv_cell)
        right  = int((screen_w - gx - ox) * inv_cell) + 1
        bottom = int((screen_h - gy - oy) * inv_cell) + 1

        layer_h = len(layer)
        layer_w = len(layer[0]) if layer else 0

        # clamp
        left = max(0, left)
        top = max(0, top)
        right = min(layer_w, right)
        bottom = min(layer_h, bottom)

        for y in range(top, bottom):
            row = layer[y]
            py = gy + y * map_cell + oy

            if py + map_cell <= 0 or py >= screen_h:
                continue

            for x in range(left, right):
                tile_key = row[x]
                if not tile_key or tile_key not in self.notation:
                    continue

                px = gx + x * map_cell + ox

                if px + map_cell <= 0 or px >= screen_w:
                    continue

                map_batches[tile_key].append([px, py, map_cell, map_cell, 0.0, 0.0])

        return map_batches


   

    def onSave(self):
        for key in self.assets_to_release:
            self.assets.delImage(key)
