from supermarioworld.package_scenes import EmptyScene
from supermarioworld.johnson import Johnson



from supermarioworld.rendering.renderer import CustomShader
from supermarioworld.rendering.easygui import TextLabel

import pygame as pg
import glm


class SubSceneEngine(EmptyScene):
    def __init__(self, game):
        super().__init__(game)
        self.shader = CustomShader(game, game.paths.ShaderPath("fragment/custom_test_1.frag"))

        self.COLOR = (255, 0, 0)
        self.TIMER = 0

        self.text_fps = TextLabel(game, self.MAIN, "fps", "FPS: ", size_font=21, color_text=self.COLOR)
        self.text_fps.setShader("shader-id", self.shader)
        self.text_fps.position = (0, 40)
        self.text_fps.layer = 99
        
        self.text_engine = TextLabel(game, self.MAIN, "engine", "Engine: Super Daemon Game Core 1.0.0", size_font=21, color_text=self.COLOR)
        self.text_engine.position = (0, 0)
        self.text_engine.layer = 99
        self.text_engine.shader_id = "shader-id"

        self.text_info = TextLabel(game, self.MAIN, "info", "Game built by DaemonDuck16", size_font=21, color_text=self.COLOR)
        self.text_info.position = (0, 20)
        self.text_info.layer = 99
        self.text_info.shader_id = "shader-id"

        

    def onRender(self):
        self.TIMER += self.game.delta_time * 2
        self.text_fps.setText(f"FPS: {self.game.getFps():.2f}", color_text=self.COLOR)

        self.shader.setUniform("time", self.TIMER)

        self.MAIN.clearPrompt()
        self.text_fps.render()
        self.text_engine.render()
        self.text_info.render()
        self.MAIN.renderSprite()




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

        self.our_y = 0
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
        self.MAIN.pushTexture("title", game.paths.ImagesPath("menu/title.png"))
        self.MAIN.pushTexture("title-border", game.paths.ImagesPath("menu/title-border.png"))
        self.MAIN.pushTexture("background", game.paths.ImagesPath("menu/background.png"))

        self.custom_test = CustomShader(game, game.paths.ShaderPath("fragment/custom_test_1.frag"))
        self.MAIN.pushShader("test-1", self.custom_test)

        self.text = TextLabel(game, self.MAIN, "text-1", "Hello World", font_path=game.paths.FontsPath("PixelFont.ttf"), size_font=32)
        self.text.position = (200, 320)
        
        
        self.text.layer = 2


    
    def onUpdate(self):
        if not self.IS_STARTED:
            self.IS_STARTED = True
            pg.mixer_music.play(-1, fade_ms=2000)
        

        # moving background
        self.our_y = glm.sin(self.timer) * 6

        self.x_1 += 36 * self.game.delta_time
        self.x_2 += 36 * self.game.delta_time

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
        r = glm.sin(self.timer * 0.8) * 0.35 + 0.65
        g = glm.sin(self.timer * 1.0 + 2.0) * 0.35 + 0.65
        b = glm.sin(self.timer * 1.2 + 4.0) * 0.35 + 0.65

        self.game.clearColor(r, g, b)
        self.timer += self.game.delta_time 
        
        self.custom_test.setUniform("time", self.timer)
        
        self.MAIN.clearPrompt()

        self.MAIN.submitSprite("background", size=(self.game.width, self.game.height), position=(self.x_1, self.our_y), layer=0)
        self.MAIN.submitSprite("background", size=(self.game.width, self.game.height), position=(self.x_2, self.our_y), layer=0)

        self.MAIN.submitSprite("title", size=(360, 160), position=(self.game.width // 2 - 180, 60), layer=4, shader="test-1")
        self.MAIN.submitSprite("title", size=(360, 160), position=(self.game.width // 2 - 180, 70), rgb=(0, 0, 0), layer=3)
        self.MAIN.submitSprite("title-border", size=(self.game.width, self.game.height), layer=5)

        self.text.render()

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
