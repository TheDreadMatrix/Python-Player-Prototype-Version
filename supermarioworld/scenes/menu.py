from supermarioworld.package_scenes import EmptyScene
from supermarioworld.johnson import Johnson


from supermarioworld.rendering.easygui import TextLabel
from supermarioworld.rendering.animation import Animation
from supermarioworld.daenums import TextureFilters



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

        self.our_y = -100
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
        self.text_play = TextLabel(game, self.RENDER, "text-1", "Play", size_font=32, font_key="pixel")
        self.text_play.position = (game.width // 2 - self.text_play.size[0] // 2 - 10, 250)
        self.text_play.rgb = (1, 1, 0)

        self.text_options = TextLabel(game, self.RENDER, "text-2", "Options", size_font=32, font_key="pixel")
        self.text_options.position = (game.width // 2 - self.text_options.size[0] // 2 - 10, 350)
        self.text_options.rgb = (1, 1, 0)

        self.text_quit = TextLabel(game, self.RENDER, "text-3", "Quit", size_font=32, font_key="pixel")
        self.text_quit.position = (game.width // 2 - self.text_quit.size[0] // 2 - 10, 450)
        self.text_quit.rgb = (1, 1, 0)
        
    
        
        self.positions = []

        for x in range(0, 48 * 17, 48):
            self.positions.append(x)
        



    
    def onUpdate(self):
        self.timer += self.game.delta_time 
        if not self.IS_STARTED:
            self.IS_STARTED = True
            pg.mixer_music.play(-1, fade_ms=1000)

        # moving background
        self.our_y = glm.sin(self.timer) * 0.7
      

        self.x_1 += 36 * self.game.delta_time
        self.x_2 += 36 * self.game.delta_time

        if self.x_1 >= self.game.width:
            self.x_1 = self.x_2 - self.game.width

        if self.x_2 >= self.game.width:
            self.x_2 = self.x_1 - self.game.width

        
        # Recolor
        if self.selected == 0:
            self.text_play.rgb = (1, 0, 0)
        else:
            self.text_play.rgb = (1, 1, 0)

        if self.selected == 1:
            self.text_options.rgb = (1, 0, 0)
        else:
            self.text_options.rgb = (1, 1, 0)

        if self.selected == 2:
            self.text_quit.rgb = (1, 0, 0)
        else:
            self.text_quit.rgb = (1, 1, 0)


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
        self.game.clearColor(0.53, 0.99, 1)
        
        
        
        self.RENDER.clearPrompt()  


        for position in self.positions:
            self.RENDER.submitSprite("b1", size=(48, 48), position=(position, 500))
            self.RENDER.submitSprite("b4", size=(48, 48), position=(position, 548))
            self.RENDER.submitSprite("b4", size=(48, 48), position=(position, 596))
        

        self.RENDER.submitSprite("background", size=(self.game.width, self.game.height), position=(self.x_1, self.our_y), layer=0)
        self.RENDER.submitSprite("background", size=(self.game.width, self.game.height), position=(self.x_2, self.our_y), layer=0)

        self.RENDER.submitSprite("title", size=(360, 160), position=(self.game.width // 2 - 180, 60), layer=4)
        self.RENDER.submitSprite("title", size=(360, 160), position=(self.game.width // 2 - 180, 70), rgb=(0, 0, 0), layer=3)
        self.RENDER.submitSprite("title-border", size=(self.game.width, self.game.height), layer=5)
        

        self.RENDER.submitSprite(self.text_play.texture_id, size=self.text_play.size, position=self.text_play.position, rgb=self.text_play.rgb)
        self.RENDER.submitSprite(self.text_options.texture_id, size=self.text_options.size, position=self.text_options.position, rgb=self.text_options.rgb)
        self.RENDER.submitSprite(self.text_quit.texture_id, size=self.text_quit.size, position=self.text_quit.position, rgb=self.text_quit.rgb)
       

        self.RENDER.renderSprite()

      

        
       
    


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




class QuitScene(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        self.request.closeGame()