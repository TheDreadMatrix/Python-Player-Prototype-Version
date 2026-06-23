import pygame as pg

from supermarioworld.johnson import readData, saveData
from supermarioworld.package_typing import GameType
from supermarioworld.scenes.base import EmptyScene

from supermarioworld.rendering.animation import AnimationCutOut
from supermarioworld.rendering.users import TextLabel



from supermarioworld.configuration import (NOTATION_BIOME_OVERWORLD, PIXEL_TILE_SIZE,
                                           PALETTE_PER_ROW, OVERWORLD_EDITOR_COLS, OVERWORLD_EDITOR_ROWS, MIN_ZOOM_EDITOR, MAX_ZOOM_EDITOR)



# TODO: Make hitbox better, Make overui rects, Make load and save system, Make notation load and save system, Content

class OverworldEditor(EmptyScene):
    def __init__(self, game: GameType, biome: int=0, index_map: int=0):
        super().__init__(game)

        self.audio.load("B-underground")
        self.audio.setFilterLowPass(8000)
        self.audio.play()


        self.cell_size = 32
        self.grid_origin = (20, 100)

        self.view_offset = [0, 0]
        self.zoom = 1.0
  

        self.palette_scroll_rows = 0

        self.palette_pos = [0, 120]
        self._drag_palette = False
        self._drag_palette_off = (0, 0)

        # Read file and atlas
        self.biome_index = biome
        notation = readData(game.paths.ConfigPath(f"overworld/notations/{NOTATION_BIOME_OVERWORLD.get(biome)}.json"))

        self.notation = notation.get("tiles", {})
        self.assets.regAtlas("overworld", notation["img-ref"])


        self.palette_keys = [k for k, _ in self.notation.items()]
        self.selected_tile = self.palette_keys[0] if self.palette_keys else None

        self.assets_to_release = set()
        self.animations: dict[str, AnimationCutOut] = {}


        # Menus
        self.menus = {
            "File": [
                ("Open", lambda: self._set_status("Soon")),
                ("Open notation", lambda: self._set_status("Soon")),
                ("Save", lambda: self._save_current_map(self.map_path)),
                ("Exit", self.request.closeGame),
            ],

            "Edit": [
                ("Undo", self._undo_last),
            ],

            "View": [
                ("Switch biome-", lambda: self._switch_biome(-1)),
                ("Switch biome+", lambda: self._switch_biome(1)),
                ("Zoom In", lambda: self._change_zoom(0.1)),
                ("Zoom Out", lambda: self._change_zoom(-0.1)),
            ],

            "Modes": [
                ("Set Node mode", lambda: self._set_status("Soon")),
                ("Set Mapso mode", lambda: self._set_status("Soon")),
                ("Set Tile mode", lambda: self._set_status("Soon"))    
            ]
        }

        self.opened_menu = None

        # Create texture and text
        self._register_palette_textures()
        self._create_labels()
        

        # Connect other files
        maps_dir = game.paths.ConfigFolder("overworld/maps")
        self.map_files = game.paths.findGlobal(maps_dir, file_category="*.json")
        self.map_index = index_map

        
        self.map_path = f"{maps_dir}/overworld-1.json"
        self.map_json = {}

        # Status
        self.status = "Ready"
        self.status_timer = 0.0

        # Mouse
        self._prev_mouse_buttons = (False, False, False)
        self._prev_mouse_pos = pg.mouse.get_pos()

        # CTRL + Z
        self.undo_stack = []
        self.dirty = False

        # Batches
        self._cached_map_batches = {}
        self._last_title = ""
    
        self._load_current_map(self.map_path)



    def _create_labels(self):
        self.menu_labels = []
        self.menu_rects = {}

        self.dropdown_labels = {}
        self.dropdown_rects = {}

        x = 10

        for menu_name in self.menus:
            label = TextLabel(self.game, text=menu_name, size_font=15, font_key="pixel")

            label.position = (x, 15)

            self.menu_labels.append({"name": menu_name, "label": label})

            self.menu_rects[menu_name] = (x, 15, label.width, label.height)

            x += label.width + 25

        x = 10

        for menu_name, items in self.menus.items():
            self.dropdown_labels[menu_name] = []
            self.dropdown_rects[menu_name] = []

            max_width = 0

            for text, callback in items:
                label = TextLabel(self.game, text=text, size_font=14, font_key="pixel")

                max_width = max(max_width, label.width)

                self.dropdown_labels[menu_name].append({"label": label, "callback": callback})

            menu_x = self.menu_rects[menu_name][0]
            menu_y = self.menu_rects[menu_name][1] + self.menu_rects[menu_name][3]

            width = max_width + 20

            for i, item in enumerate(self.dropdown_labels[menu_name]):
                rect = (menu_x, menu_y + i * 24, width, 50)

                item["label"].position = (menu_x + 5, menu_y + i * 24 + 20)

                self.dropdown_rects[menu_name].append(rect)

        


        self.status_label = TextLabel(self.game, size_font=15, font_key="pixel")
        self.status_label.position = (self.game.width * 0.37, 15)



    def _register_palette_textures(self):
        for tile_key in self.palette_keys:
            tile = self.notation[tile_key]

            if isinstance(tile, dict) and "frames" in tile:
                # ANIMATION
                key_images = [f"{tile_key}_{i}" for i in range(len(tile["frames"]))]

                anim = AnimationCutOut(game=self.game, key_atlas="overworld",
                    frames=[(*f.get("xy", (0, 0)), *f.get("wh", (PIXEL_TILE_SIZE, PIXEL_TILE_SIZE))) for f in tile["frames"]],
                    durations=tile.get("durations", [0.1] * len(tile["frames"])),
                    key_images=key_images,
                )

                self.animations[tile_key] = anim
            else:
                if isinstance(tile, list):
                    x, y = tile
                    w, h = (PIXEL_TILE_SIZE, PIXEL_TILE_SIZE)
                else:
                    x, y = tile.get("xy", (0, 0))
                    w, h = tile.get("wh", (PIXEL_TILE_SIZE, PIXEL_TILE_SIZE))


                self.assets.regCutOutImage(tile_key, "overworld", x=x, y=y, w=w, h=h)
                self.assets_to_release.add(tile_key)



    def _load_current_map(self, path):
        self.map_json = readData(path)
        
        
        self._normalize_active_layer()
        self.dirty = False
        self.status = f"Loaded: {path}"
    

    def _normalize_active_layer(self):
        if not self.map_json.get("tile-map-world"):
            self.map_json["tile-map-world"] = []
            
        layer = self.map_json["tile-map-world"]
        default_tile = "tile-1" if "tile-1" in self.notation else ""
        is_completely_empty = all((not cell) for row in layer for cell in row) if layer else True

        
        while len(layer) < OVERWORLD_EDITOR_ROWS:
            layer.append([])

        width = max((len(row) for row in layer), default=0)
        width = max(width, OVERWORLD_EDITOR_COLS)
        for row in layer:
            while len(row) < width:
                row.append(default_tile if is_completely_empty else "")


    def _active_layer(self):
        return self.map_json.get("tile-map-world", [])


    def _set_status(self, text: str):
        self.status = text
        self.status_timer = 9.0

    def _switch_map(self, delta: int):
        if not self.map_files:
            return
        self.map_index = (self.map_index + delta) % len(self.map_files)
        self._load_current_map()


    def _switch_biome(self, delta: int):
        biome_count = len(NOTATION_BIOME_OVERWORLD)
        self.biome_index = (self.biome_index + delta) % biome_count

       
        for anim in self.animations.values():
            anim.delAnimation()

        self.animations.clear()

     
        for key in self.assets_to_release:
            self.assets.delImage(key)

        self.assets_to_release.clear()

       
        notation = readData(self.game.paths.ConfigPath(f"overworld/notations/{NOTATION_BIOME_OVERWORLD[self.biome_index]}.json"))

        self.notation = notation.get("tiles", {})

        
        self.assets.regAtlas("overworld", notation.get("img-ref", ""))

      
        self.palette_keys = list(self.notation.keys())
        self.selected_tile = self.palette_keys[0] if self.palette_keys else None

      
        self._register_palette_textures()

        self._normalize_active_layer()

        self._set_status(f"Biome: {NOTATION_BIOME_OVERWORLD[self.biome_index]}")



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

        
        current = layer[ty][tx]
        new_value = "" if erase else self.selected_tile
        if current == new_value:
            return False

        self.undo_stack.append((tx, ty, current))
        layer[ty][tx] = new_value
        self.dirty = True

        return True

    def _undo_last(self):
        if not self.undo_stack:
            self._set_status("Nothing to undo")
            return

        tx, ty, prev_value = self.undo_stack.pop()
        layer = self.map_json.get("tile-map-world", [])
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
        for rect in self.menu_rects.values():
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

    def _save_current_map(self, path):
        saveData(path, self.map_json)
        self.dirty = False
        self._set_status("Saved")

    def onUpdate(self):
        for animation in self.animations.values():
            animation.update()

        if self.status_timer > 0:
            self.status_timer -= self.game.delta_time
        else:
            self.status = "LMB draw | RMB erase | Ctrl+S save"

        self._handle_mouse_input()

        title = f"SMW91: {self.map_path if self.map_path else 'none'} {'*' if self.dirty else ''}"

        if title != self._last_title:
            self.request.setTitle(title)
            self._last_title = title

        
        self.status_label.setText(self.status, r_text=1, g_text=1, b_text=1)
        


    def _handle_mouse_input(self):
        mouse_pos = pg.mouse.get_pos()
        left, middle, right = pg.mouse.get_pressed(3)
        prev_left, prev_middle, prev_right = self._prev_mouse_buttons


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
            

       
        if left and not middle and not over_ui and not over_palette:
            if self._paint(mouse_pos, erase=False):
                self._set_status("Draw")

        if right and not middle and not over_ui and not over_palette and self._paint(mouse_pos, erase=True):
            self._set_status("Erase")

        self._prev_mouse_buttons = (left, middle, right)
        self._prev_mouse_pos = mouse_pos


    def onEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = event.pos

                for menu_name, rect in self.menu_rects.items():
                    if self._in_rect(mouse_pos, rect):
                        if self.opened_menu == menu_name:
                            self.opened_menu = None
                        else:
                            self.opened_menu = menu_name
                        return
                    
                if self.opened_menu:
                    for item, rect in zip(self.dropdown_labels[self.opened_menu], self.dropdown_rects[self.opened_menu]):
                        if self._in_rect(mouse_pos, rect):
                            item["callback"]()
                            self.opened_menu = None
                            return

            self.opened_menu = None
                        
            
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s and (event.mod & pg.KMOD_CTRL):
                self._save_current_map(self.map_path)
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
        self.zoom = max(MIN_ZOOM_EDITOR, min(MAX_ZOOM_EDITOR, self.zoom + delta))
        

    def _pick_tile_from_palette(self, pos):
        if not self._in_rect(pos, self._palette_view_rect()):
            return False
        for tile_key, rect in self._palette_rects():
            if self._in_rect(pos, rect):
                self.selected_tile = tile_key
                self._set_status(f"Tile: {self.selected_tile}")
                return True
        return False

    def onRender(self):
        self._cached_map_batches = self._build_map_batches()
        

        self.game.clearColor(0.5, 0.5, 0.5)

        for texture_key, instances in self._cached_map_batches.items():
            self.renderer.renderInstance(texture_key, instances=instances)

        
        view_x, view_y, view_w, view_h = self._palette_view_rect()

        self.renderer.renderQuad(position=(view_x, view_y), size=(view_w, view_h), r=0.1, g=0.2, b=0.1, a=0.7)

        for tile_key, rect in self._palette_rects():
            x, y, w, h = rect
            if y + self.cell_size <= view_y or y >= view_y + view_h:
                continue

            tex = self._get_texture_key(tile_key)
            if isinstance(self.notation[tile_key], list): 
                flx, fly = (0, 0)
            else:
                flx = self.notation[tile_key].get("flx", 0)
                fly = self.notation[tile_key].get("fly", 0)

        

            self.renderer.render(tex, position=(x, y), size=(self.cell_size, self.cell_size), flx=flx, fly=fly)
            

            if self.selected_tile == tile_key:
                self.renderer.renderQuad(position=(x, y), size=(w, h), r=1, g=0, b=0, a=0.5)
            

        



        
        self.renderer.renderQuad(size=(self.game.width, 55), r=0.1, g=0.1, b=0.1, a=0.75)
        for label in self.menu_labels:
            label["label"].render()

        if self.opened_menu:
            for item, rect in zip(self.dropdown_labels[self.opened_menu], self.dropdown_rects[self.opened_menu]):
                x, y, w, h = rect

                self.renderer.renderQuad(position=(x, y), size=(w, h), r=0.15, g=0.15, b=0.15, a=0.95)

                item["label"].render()

        
      
        self.status_label.render()
        

        
       
    def _get_texture_key(self, tile_key):
        if tile_key in self.animations:
            return self.animations[tile_key].getTextureKey()
        return tile_key

            

    def _build_map_batches(self):
        batches = {}

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

                tex = self._get_texture_key(tile_key)
                if isinstance(self.notation[tile_key], list): 
                    flx, fly = (0, 0)
                else:
                    flx = self.notation[tile_key].get("flx", 0)
                    fly = self.notation[tile_key].get("fly", 0)
                    
                batches.setdefault(tex, []).append([px, py, map_cell, map_cell, flx, fly])

        return batches



    def onSave(self):
        for animation in self.animations.values():
            animation.delAnimation()

        for key in self.assets_to_release:
            self.assets.delImage(key)
