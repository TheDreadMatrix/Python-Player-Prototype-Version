from supermarioworld.package_typing import EmptyScene
from supermarioworld.johnson import Johnson

from supermarioworld.rendering.moderngl import load_texture

import pygame as pg
import glm





class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        #MUSIC
        pg.mixer_music.load(game.paths.MusicPath("title-name.mp3"))
        pg.mixer_music.play(-1, fade_ms=2000)
        pg.mixer_music.set_volume(self.game.settings_read["music"])

        self.sound_choose = pg.mixer.Sound(game.paths.SoundPath("map.wav"))
        self.sound_cancer = pg.mixer.Sound(game.paths.SoundPath("pause.wav"))
        self.sound_pointer = pg.mixer.Sound(game.paths.SoundPath("pointer.mp3"))

        #JSON DATAS
        self.account_0 = Johnson(game.paths.ConfigPath("player-info/player0.json")).readData()
        self.account_1 = Johnson(game.paths.ConfigPath("player-info/player1.json")).readData()
        self.account_2 = Johnson(game.paths.ConfigPath("player-info/player2.json")).readData()
        self.account_dict = {f"P-{i}": f"player-info/player{i}" for i in range(3)}

        #ATTRIBUTES
        self.timer_appear = 0
        self.timer_dissappear = 1
        self.x_1, self.x_2 = 0, self.game.width

        self.alpha = 0
        self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
        self.selected = 0

        self.active = glm.vec3(1, 1, 0)   
        self.inactive = glm.vec3(1, 1, 1)

        self.switch_timer = 0
        self.switch_delay = 2.5
        self.switching = False
        self.switching_game = False
        self.switch_target_scene = ""

        
    def onUpdate(self):
        self.x_1 += 12 * self.game.delta_time
        self.x_2 += 12 * self.game.delta_time

        if self.x_1 >= self.game.width:
            self.x_1 = self.x_2 - self.game.width

        if self.x_2 >= self.game.width:
            self.x_2 = self.x_1 - self.game.width

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
                    self.game.settings_read["current-player-account-path"] = self.account_dict[self.options[self.selected]]
                    self.switching = True
                    self.switch_timer = 0
                    self.switch_target_scene = "cutscene"

   
            if event.key == pg.K_z and self.switching_game:
                self.sound_cancer.play()
                self.switching_game = False
                self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
                self.selected = 0

        
            
        
    
    def onRender(self):
        pass

       
    


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
