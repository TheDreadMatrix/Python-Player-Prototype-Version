from MyEngine.GameClasses.DataClasses import Sounds, Image
from MyEngine.GameClasses.Animates import Animates
from MyEngine.GameClasses.Interfaces import MainObject, KinematicObject
from MyEngine.GameObjects.Camera import RegionCamera
from MyEngine.Utils.joshua import load, de_load, load_anim, Joshua
from MyEngine.Utils.settings import pg, BLACK, WHITE, RED, SCREEN_HEIGHT, SCREEN_WIDTH, SCL, DOB, PREFIX_GAME, font
from MyEngine.Utils.ui_tools import Button
from MyEngine.Utils.physic import Physic
import gc


pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=SCL|DOB)
pg.display.set_caption("Editor Level: 0.1.0", "Editor Level: 1.0.0")
#pg.mixer.music.load(f"{PREFIX_GAME}MusicAndSound/overworld_music.mp3")
#pg.mixer.music.play(-1, fade_ms=1200)

PREFIX = "MyEngine/Assets/Tile-Blocks/"
PRESPR = "MyEngine/Assets/ObjectSprite/"

TILE_SIZE = 64

solid_1 = Image(load(f"{PREFIX}grass_block_4.png").convert_alpha())
solid_2 = Image(load(f"{PREFIX}grass_block_1.png").convert_alpha())
solid_3 = Image(de_load(solid_1.image, flip_x=True).convert_alpha())
solid_4 = Image(load(f"{PREFIX}grass_block_3.png").convert_alpha())
solid_5 = Image(load(f"{PREFIX}grass_block_2.png").convert_alpha())
solid_6 = Image(de_load(solid_4.image, flip_x=True).convert_alpha())
solid_7 = Image(de_load(solid_1.image, flip_y=True).convert_alpha())
solid_8 = Image(de_load(solid_2.image, flip_y=True).convert_alpha())
solid_9 = Image(de_load(solid_1.image, flip_x=True, flip_y=True).convert_alpha())

solid_10 = Image(load(f"{PREFIX}grass_block_5.png").convert_alpha())
solid_11 = Image(de_load(solid_10.image, flip_x=True).convert_alpha())
solid_12 = Image(de_load(solid_10.image, flip_y=True).convert_alpha())
solid_13 = Image(de_load(solid_10.image, flip_x=True, flip_y=True).convert_alpha())
solid_14 = Image(load(f"{PREFIX}grass_block_6.png").convert_alpha())
solid_15 = Image(de_load(solid_14.image, flip_x=True).convert_alpha())

one_1 = Image(load(f"{PREFIX}moun_block_4.png").convert_alpha())
one_2 = Image(load(f"{PREFIX}moun_block_1.png").convert_alpha())
one_3 = Image(de_load(one_1.image, flip_x=True).convert_alpha())

water_1 = load_anim(f"{PREFIX}water_block.gif", (64, 64), fps=5)
water_2 = Image(load(f"{PREFIX}water_block_r.png").convert_alpha())

lava_1 = Image(load("").convert_alpha())
lava_2 = Image(load("").convert_alpha())

climb_1 = Image(load(f"{PREFIX}climb_block_1.png").convert_alpha())
climb_2 = Image(de_load(climb_1.image, flip_x=True).convert_alpha())
climb_3 = Image(de_load(climb_1.image, flip_y=True).convert_alpha())
climb_4 = Image(de_load(climb_1.image, flip_x=True, flip_y=True).convert_alpha())

slope_1 = Image(load(f"{PREFIX}grass_slop_1.png").convert_alpha())
slope_2 = Image(de_load(slope_1.image, flip_x=True).convert_alpha())
slope_3 = Image(load("").convert_alpha())
slope_4 = Image(load("").convert_alpha())
slope_5 = Image(load("").convert_alpha())
slope_6 = Image(load("").convert_alpha())

pointer_1 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_2 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_3 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_4 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_5 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_6 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_7 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_8 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_9 = Image(load(f"{PREFIX}pointer.png").convert_alpha())
pointer_10 = Image(load(f"{PREFIX}pointer.png").convert_alpha())

coin_block_1 = Image(load(f"{PREFIX}new_support.png").convert_alpha())
coin_block_2 = Image(load(f"{PREFIX}new_support.png").convert_alpha())
coin_block_3 = Image(load(f"{PREFIX}new_support.png").convert_alpha())

roin_block_1 = Image(load(f"{PREFIX}new_support.png").convert_alpha())
roin_block_2 = Image(load(f"{PREFIX}new_support.png").convert_alpha())
roin_block_3 = Image(load(f"{PREFIX}new_support.png").convert_alpha())

cape_block = Image(load(f"{PREFIX}new_support.png").convert_alpha())
fire_block = Image(load(f"{PREFIX}new_support.png").convert_alpha())
super_block = Image(load(f"{PREFIX}new_support.png").convert_alpha())
default_block = Image(load(f"{PREFIX}new_support.png").convert_alpha())
health_block = Image(load(f"{PREFIX}new_support.png").convert_alpha())
broken_block = Image(load(f"{PREFIX}new_support.png").convert_alpha())

save_img = load(f"MyEngine/Assets/Stuff/save_btn.png").convert_alpha()
load_img = load(f"MyEngine/Assets/Stuff/load_btn.png").convert_alpha()



blocks = [
    solid_1, solid_2, solid_3, solid_4, solid_5, solid_6, solid_7, solid_8, solid_9,
    solid_10, solid_11, solid_12, solid_13, solid_14, solid_15,
    one_1, one_2, one_3,
    water_1, water_2,
    lava_1, lava_2,
    climb_1, climb_2, climb_3, climb_4,
    slope_1, slope_2, slope_3, slope_4, slope_5, slope_6,
    pointer_1, pointer_2, pointer_3, pointer_4, pointer_5,
    pointer_6, pointer_7, pointer_8, pointer_9, pointer_10,
    coin_block_1, coin_block_2, coin_block_3,
    roin_block_1, roin_block_2, roin_block_3,
    cape_block, fire_block, super_block, default_block,
    health_block, broken_block
]

for block in blocks:
    if not isinstance(block, Animates):
        block.scale((TILE_SIZE, TILE_SIZE))



coin = Image(load(f"{PRESPR}coin.gif").convert_alpha())
roin = None

cape = None
fire = Image(load(f"{PRESPR}flower.gif").convert_alpha())
super = Image(load(f"{PRESPR}mushroom.gif").convert_alpha())
default = None
health = None

trampoline = None
door_1 = Image(load(f"{PRESPR}door.png").convert_alpha())

enemy_11 = None
enemy_12 = None

enemy_21 = None
enemy_22 = None

enemy_31 = None
enemy_32 = None

enemy_41 = None
enemy_42 = None





class LevelEditor(MainObject):
    def __init__(self):
        self.img_dict = {}
        self.count = 1

        self.data = Joshua(f"{PREFIX_GAME}/DataGame/level_{self.count}.json")
        self.data_read = self.data.read_data()
        self.new_data = None

        self.data_world = []
        self.rows = 27
        self.max_rows = 512

        self.button_list = []
        self.button_col = 0
        self.button_row = 0

        self.current_tile = "0"
        self.offset_mouse = 0


        self.UI_board = pg.Rect(screen.get_width() - 450, 0, 700, screen.get_height() + 100)
        self.UI_takeboard = pg.Rect(0, screen.get_height() - 200, screen.get_width(), 200)   
        self.__init_on()

        self.init_map()


    def init_map(self):
        for row in range(self.rows):
            r = ["0"] * self.max_rows
            self.data_world.append(r)

        for  tile in range(0, self.max_rows):
            self.data_world[self.rows - 9][tile] = "2"
            self.data_world[self.rows - 8][tile] = "5"
            self.data_world[self.rows - 7][tile] = "5"
            self.data_world[self.rows - 6][tile] = "5"
            self.data_world[self.rows - 5][tile] = "5"
            self.data_world[self.rows - 4][tile] = "5"
            self.data_world[self.rows - 3][tile] = "5"
            self.data_world[self.rows - 2][tile] = "5"
            self.data_world[self.rows - 1][tile] = "5"



    def __init_on(self):
        self.save_btn = Button(screen.get_width() - 1000 , screen.get_height() - 180, save_img.get_width(), save_img.get_height(), save_img, 1)
        self.load_btn = Button(screen.get_width() - 800, screen.get_height() - 180, load_img.get_width(), load_img.get_height(), load_img, 1)
        self.up_btn = Button(screen.get_width() - 600, screen.get_height() - 180, 200, 50, pg.Surface((200, 50)), 1)
        self.down_btn = Button(screen.get_width() - 600, screen.get_height() - 130, 200, 50, pg.Surface((200, 50)), 1)

        self.img_dict.update({
    "1": solid_1,
    "2": solid_2,
    "3": solid_3,
    "4": solid_4,
    "5": solid_5,
    "6": solid_6,
    "7": solid_7,
    "8": solid_8,
    "9": solid_9,
    "10": solid_10,
    "11": solid_11,
    "12": solid_12,
    "13": solid_13,
    "14": solid_14,
    "15": solid_15,

    "o1": one_1,
    "o2": one_2,
    "o3": one_3,

    "w1": water_1,
    "w2": water_2,

    "l1": lava_1,
    "l2": lava_2,

    "cl1": climb_1,
    "cl2": climb_2,
    "cl3": climb_3,
    "cl4": climb_4,

    "s1": slope_1,
    "s2": slope_2,
    "s3": slope_3,
    "s4": slope_4,
    "s5": slope_5,
    "s6": slope_6,

    "@br": broken_block,
    "@ca": cape_block,
    "@fi": fire_block,
    "@de": default_block,
    "@sp": super_block,
    "@hp": health_block,

    "@cn": coin_block_1,
    "@Cn": coin_block_2,
    "@CN": coin_block_3,

    "@rc": roin_block_1,
    "@Rc": roin_block_2,
    "@RC": roin_block_3,

    "@p1": pointer_1,
    "@p2": pointer_2,
    "@p3": pointer_3,
    "@p4": pointer_4,
    "@p5": pointer_5,
    "@p6": pointer_6,
    "@p7": pointer_7,
    "@p8": pointer_8,
    "@p9": pointer_9,
    "@p10": pointer_10,

    "cn": coin,
    "fi": fire,
    "sp": super,
    "dr1": door_1
})
        

        for key, image in self.img_dict.items():
            btn = Button(
            screen.get_width() - 400 + (75 * self.button_col),   # x
                50 + 75 * self.button_row,                          # y
                    TILE_SIZE,
                    TILE_SIZE,
                    image.image, 1)
            self.button_list.append((key, btn))

            self.button_col += 1
            if self.button_col == 5:
                self.button_row += 2
                self.button_col = 0

    
    def update(self, **kwargs):
        pos = pg.mouse.get_pos()  
        mouse_buttons = pg.mouse.get_pressed()

        x = int((pos[0] + camera.offset.x) // 64)
        y = int((pos[1] + camera.offset.y) // 64 - 4)

        if pos[0] < 800 and pos[1] < 450:
            if mouse_buttons[0]:
                if 0 <= y < self.rows and 0 <= x < self.max_rows:
                    self.data_world[y][x] = self.current_tile

            if mouse_buttons[2]:
                if 0 <= y < self.rows and 0 <= x < self.max_rows:
                    self.data_world[y][x] = "0"


    
    def handler_event(self, event):
        if event.type == pg.MOUSEWHEEL:
            for key, btn in self.button_list:
                btn.rect.y += event.y * 30
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.up_btn.hover:
                self.count += 1
                self.count = min(8, self.count)
                self.data = Joshua(f"{PREFIX_GAME}/DataGame/level_{self.count}.json")
               
            if event.button == 1 and self.down_btn.hover:
                self.count -= 1
                self.count = max(1, self.count)
                self.data = Joshua(f"{PREFIX_GAME}/DataGame/level_{self.count}.json")
               
        


    def render(self, **kwargs):
        for c in range(self.max_rows):
            pg.draw.line(screen, (255, 255, 255),
                     (round(c * TILE_SIZE - camera.offset.x), 0), (round(c * TILE_SIZE - camera.offset.x), screen.get_height()))

        for c in range(self.rows):
            pg.draw.line(screen, (255, 255, 255),
                     (0, round(c * TILE_SIZE - camera.offset.y)), (screen.get_width(), round(c * TILE_SIZE - camera.offset.y)))
            
        for y, row in enumerate(self.data_world):
            for x, tile in enumerate(row):
                if tile == "0":
                    continue

                
                if camera.camera_box.colliderect(self.img_dict[tile].image.get_frect(topleft=(x * TILE_SIZE, y * TILE_SIZE + 256))):

                    if isinstance(self.img_dict[tile].image, pg.Surface):
                        screen.blit(self.img_dict[tile].image, (round(x * TILE_SIZE - camera.offset.x), round((y * TILE_SIZE + 256) - camera.offset.y)))
                    else:
                        self.img_dict[tile].image.animate(surface=screen,
                            coord=(x * TILE_SIZE - camera.offset.x, (y * TILE_SIZE + 256) - camera.offset.y))

        
        #pg.draw.rect(screen, (0, 150, 150), self.UI_board)
        #pg.draw.rect(screen, (0, 150, 150), self.UI_takeboard)

        for key_tile, btn in self.button_list:
            if btn.draw(screen, dt=dt):
                self.current_tile = key_tile

            if key_tile == self.current_tile:
                pg.draw.rect(screen, (255, 0, 0), (btn.rect.x, btn.rect.y, btn.rect.w, btn.rect.h), width=3)


        if self.save_btn.draw(screen, dt=dt):
            self.data_read["tile-map"] = self.data_world
            self.data.save_data(self.data_read)

        if self.load_btn.draw(screen, dt=dt):
            self.new_data = self.data.read_data()
            self.data_world = self.new_data["tile-map"]
            person.rect.x = 0
            person.rect.y = 300


        self.up_btn.draw(screen, dt=dt)
        self.down_btn.draw(screen, dt=dt)




    def dispose(self):
        self.__dict__.clear()

        gc.collect()
    



class Person(KinematicObject):
    def __init__(self, pos, app, img, **kwargs):
        self.app = app
        self.rect = pg.FRect(pos)
        self.img = img
        self.velocity = pg.Vector2(0, 0)
        self.__init_on()

    def __init_on(self):
        self.physic = Physic(rectangle=self.rect, velocity=self.velocity)

    def update(self, **kwargs):
        key = pg.key.get_pressed()

        if key[pg.K_d]:
            self.physic.add_velocity_x("x+", delta_time=dt, max_speed=500)
        elif key[pg.K_a]:
            self.physic.add_velocity_x("x-", delta_time=dt, max_speed=500)
        else:
            self.physic.dispose("x")

        if key[pg.K_w]:
            self.physic.add_velocity_y("y-", max_speed=500)
        elif key[pg.K_s]:
            self.physic.add_velocity_y("y+", max_speed=500)
        else:
            self.physic.dispose("y")

        self.physic.move("x", delta_time=dt)
        self.physic.move("y", delta_time=dt)

        self.collision()
            

    
    def collision(self, **kwargs):
        if self.rect.x < 0:
            self.rect.x = 0
    
    def render(self, camera_offset):
        pg.draw.rect(screen, RED, (round(self.rect.x - camera_offset.x), round(self.rect.y - camera_offset.y), self.rect.w, self.rect.h), width=3)



    
    def dispose(self):
        self.__dict__.clear()

        gc.collect()






leditor = LevelEditor()
camera = RegionCamera()
person = Person(pos=(0, 200, 64, 64), app=0, img=None)

clock = pg.time.Clock()
run = True
while run:
    dt = min(clock.tick() / 1000, 0.05)
    screen.fill(BLACK)
    camera.scroll(surface=screen, target_rect=person.rect, delta_time=dt, scroll_y=2000, scroll_x=32768, velocity=person.velocity)
    #camera.render(surface=screen)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        leditor.handler_event(event=event)


    leditor.update()
    person.update()

    leditor.render()
    person.render(camera_offset=camera.offset)


   
    fps_text = font.render(f"FPS {int(clock.get_fps())}", True, WHITE)
    current_tile = font.render(f"Current-Tile: {leditor.current_tile} - CFM: {leditor.count}", True, RED)
    coord = font.render(f"X: {person.rect.x} - Y: {person.rect.y}", True, RED)

    
    screen.blit(fps_text, (5, 5))
    screen.blit(current_tile, (50, 50))
    screen.blit(coord, (50, 75))



    pg.display.flip()

leditor.dispose()
person.dispose()    
pg.quit()