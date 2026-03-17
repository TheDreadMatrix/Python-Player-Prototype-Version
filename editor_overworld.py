from MyEngine.GameClasses.DataClasses import Image, Sounds
from MyEngine.GameClasses.Interfaces import MainObject, KinematicObject
from MyEngine.GameObjects.Camera import RegionCamera
from MyEngine.Utils.physic import Physic
from MyEngine.Utils.joshua import load, de_load, load_anim, Joshua
from MyEngine.Utils.settings import pg, sys, WHITE, BLACK, RED, SCREEN_HEIGHT, SCREEN_WIDTH, font
from numba import njit


pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pg.DOUBLEBUF|pg.SCALED)
pg.display.set_caption("Editor OverWorld: 0.1.0", "Editor OverWorld")
pg.mixer.music.load("MyEngine/MusicAndSound/overworld_music_2.mp3")
pg.mixer.music.play()

#===========================
#object in layer 2:
PREFIX = "MyEngine/Assets/Tile-Blocks/"
TILE_SIZE = 32


star = Image(load(f"{PREFIX}str.png")).image.convert_alpha()
home = Image(load(f"{PREFIX}hm.png")).image.convert_alpha()

fortress = Image(load(f"{PREFIX}cs_1.png")).image.convert_alpha()

little_level_1 = Image(load(f"{PREFIX}ll_1.png")).image.convert_alpha()
little_level_2 = Image(load(f"{PREFIX}ll_2.png")).image.convert_alpha()

greater_level_1 = Image(load(f"{PREFIX}gl_1.png")).image.convert_alpha()
greater_level_2 = Image(load(f"{PREFIX}gl_2.png")).image.convert_alpha()
greater_water = Image(load(f"{PREFIX}gw.png")).image.convert_alpha()
greater_none = Image(load(f"{PREFIX}gn.png")).image.convert_alpha()

greater_rock = Image(load(f"{PREFIX}gr_1.png")).image.convert_alpha()

road_1 = Image(load(f"{PREFIX}r1.png")).image.convert_alpha()
road_2 = Image(load(f"{PREFIX}r2.png")).image.convert_alpha()

pipe = Image(load(f"{PREFIX}pp.png")).image.convert_alpha()


#pre-objects in layer 1:
grass_0 = Image(load(f"{PREFIX}grass_0.png")).image.convert_alpha()



class Editor(MainObject):
    def __init__(self, tile_map_obj, tile_map_pre):
        self.img_dict = {}

        self.data_world = []
        self.rows = 32
        self.max_rows = 64

        self.__init_on()
        self.init_map()


    def init_map(self):
        for row in range(self.rows):
            r = ["0"] * self.max_rows
            self.data_world.append(r)

        for  tile in range(0, self.max_rows):
            self.data_world[self.rows - 10][tile] = "r1"
            self.data_world[self.rows - 9][tile] = "r2"
            self.data_world[self.rows - 8][tile] = "r2"
            self.data_world[self.rows - 7][tile] = "r2"
            self.data_world[self.rows - 6][tile] = "r2"
            self.data_world[self.rows - 5][tile] = "r2"
            self.data_world[self.rows - 4][tile] = "r2"
            self.data_world[self.rows - 3][tile] = "r2"
            self.data_world[self.rows - 2][tile] = "r2"

        


    def __init_on(self):
        self.img_dict.update({"r1": road_1, "r2": road_2, "ll1": little_level_1, "ll2": little_level_2, "gl1": greater_level_1, "gl2": greater_level_2})
        self.img_dict.update({})
    

    def update(self, **kwargs):
        return super().update(**kwargs)
    
    def handler_event(self, event):
        return super().handler_event(event)
    

    def render(self, **kwargs):
        for y, row in enumerate(self.data_world):
            for x, tile in enumerate(row):
                if tile == "0":
                    continue

                screen.blit(self.img_dict[tile], (round(x * 32 - region.offset.x), round(y * 32 - region.offset.y)))

        screen.blit(font.render(f"FPS {clock.get_fps()}", True, RED), (5, 5))
        

    def grind(self):
        for c in range(self.max_rows):
            pg.draw.line(screen, WHITE,
                     (round(c * TILE_SIZE - region.offset.x), 0), (round(c * TILE_SIZE - region.offset.x), screen.get_height()))

        for c in range(self.rows + 5):
            pg.draw.line(screen, WHITE,
                     (0, round(c * TILE_SIZE - region.offset.y)), (screen.get_width(), round(c * TILE_SIZE - region.offset.y)))
        return 
    

    def dispose(self):
        return super().dispose()
    







class Person(KinematicObject):
    def handler_input(self):
        pass


    def collision(self, **kwargs):
        return super().collision(**kwargs)
    

    def render(self, camera_offset):
        return super().render(camera_offset)
    
    def dispose(self):
        return super().dispose()
    











#Init...
region = RegionCamera()
editor = Editor(Joshua("MyEngine/DataGame/overworld_map.json").read_data()["ovw-1"]["obj"], 
                Joshua("MyEngine/DataGame/overworld_map.json").read_data()["ovw-1"]["pre"])




person = Person(pos=(100, 400, 64, 64), app=None, img=None)


clock = pg.time.Clock()
is_run = True


while is_run:
    dt = clock.tick() / 1000
    screen.fill(BLACK)
    region.scroll(surface=screen, delta_time=dt)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_run = False


    
    editor.grind()
    editor.render()


    if pg.time.get_ticks() % 1000 < 16:  
        fps_text = font.render(f"FPS {int(clock.get_fps())}", True, RED)
        screen.blit(fps_text, (5, 5))




    pg.display.flip()
pg.quit()
sys.exit()
