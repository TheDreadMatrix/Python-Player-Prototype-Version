from supermarioworld.package_scenes import EmptyScene
from supermarioworld.johnson import Johnson

from supermarioworld.rendering.moderngl import load_texture

import pygame as pg
import glm





class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        #MUSIC
        self.IS_STARTED = False
        pg.mixer_music.load(game.paths.MusicPath("title-name.mp3"))
        pg.mixer_music.set_volume(self.game.settings_read["music"])
        

        self.sound_choose = pg.mixer.Sound(game.paths.SoundPath("map.wav"))
        self.sound_cancer = pg.mixer.Sound(game.paths.SoundPath("pause.wav"))
        self.sound_pointer = pg.mixer.Sound(game.paths.SoundPath("pointer.mp3"))

        #JSON DATAS
        self.account_0 = Johnson(game.paths.CsavesPath("player/player0.json")).readData()
        self.account_1 = Johnson(game.paths.CsavesPath("player/player1.json")).readData()
        self.account_2 = Johnson(game.paths.CsavesPath("player/player2.json")).readData()
        self.account_dict = {f"P-{i}": f"player/player{i}" for i in range(3)}

        #ATTRIBUTES
        self.timer_appear = 0
        self.timer_dissappear = 1
        self.x_1, self.x_2 = 0, self.game.width

        self.alpha = 0
        self.timer = 0
        self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
        self.selected = 0

        self.switch_timer = 0
        self.switch_delay = 2.5
        self.switching = False
        self.switching_game = False
        self.switch_target_scene = ""


        # SPRITES
        self.texture_title = load_texture(game, game.paths.ImagesPath("menu/title.png"))
        self.texture_title_board = load_texture(game, game.paths.ImagesPath("menu/title-border.png"))
        self.texture_background = load_texture(game, game.paths.ImagesPath("menu/background.png"))


    
    def onUpdate(self):
        self.game.setCaption(f"{self.game.getFps()}")

        

        if not self.IS_STARTED:
            self.IS_STARTED = True
            pg.mixer_music.play(-1, fade_ms=2000)
        

        # moving background
        self.x_1 += 24 * self.game.delta_time
        self.x_2 += 24 * self.game.delta_time

        if self.x_1 >= self.game.width:
            self.x_1 = self.x_2 - self.game.width

        if self.x_2 >= self.game.width:
            self.x_2 = self.x_1 - self.game.width

        


        # fade effect
        if self.alpha != 1:
            self.timer_appear += self.game.delta_time * 0.6
            self.alpha = glm.clamp(0, self.timer_appear, 1)

        if self.switching:
            self.timer_dissappear -= self.game.delta_time * 0.6
            self.alpha = glm.clamp(self.timer_dissappear, 0.0, 1.0)
            pg.mixer_music.fadeout(2500)

            
            self.switch_timer += self.game.delta_time

            if self.switch_timer >= self.switch_delay and self.switch_target_scene:
                self.game.request.redirectScene(self.switch_target_scene)



        
            
    def onEvent(self, event):   
        if self.switching:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.sound_choose.play()
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.options) - 1 

            elif event.key == pg.K_s:
                self.sound_choose.play()
                self.selected += 1
                if self.selected >= len(self.options):
                    self.selected = 0

            if event.key == pg.K_q:
                self.sound_pointer.play()
                if not self.switching_game:
                    selected_option = self.options[self.selected]

                    if selected_option == "PLAY MODE":
                        self.switching_game = True
                        self.options = ["P-0", "P-1", "P-2"]
                        self.selected = 0

                    else:
                        self.switching = True
                        self.switch_timer = 0
                        self.switch_target_scene = "settings" if selected_option == "SETTINGS" else "quit"

                else:
                    self.game.settings_read["current-player"] = self.account_dict[self.options[self.selected]]
                    self.switching = True
                    self.switch_timer = 0
                    self.switch_target_scene = "cutscene-1"

   
            if event.key == pg.K_z and self.switching_game:
                self.sound_cancer.play()
                self.switching_game = False
                self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
                self.selected = 0

        
            
        
    
    def onRender(self):
        self.game.clearColor(0.3, 0.4, 0.8)
        
        self.MAIN.clearPrompt()

        self.MAIN.submitSprite(self.texture_background, size=(self.game.width, self.game.height), position=(self.x_1, 0), layer=0)
        self.MAIN.submitSprite(self.texture_background, size=(self.game.width, self.game.height), position=(self.x_2, 0), layer=0)

        self.MAIN.submitSprite(self.texture_title, size=(360, 160), position=(self.game.width // 2 - 180, 60), layer=2)
        self.MAIN.submitSprite(self.texture_title, size=(360, 160), position=(self.game.width // 2 - 180, 70), rgb=(0, 0, 0), layer=1)
        self.MAIN.submitSprite(self.texture_title_board, size=(self.game.width, self.game.height), layer=3)

        self.MAIN.renderSprite()

       
    


class Settings(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

    def onUpdate(self):
        pass
    
    def onEvent(self, event):
        pass
    
    def onRender(self):
        self.game._ctx.clear(0, 1, 0)
    
    def onSave(self):
        pass
