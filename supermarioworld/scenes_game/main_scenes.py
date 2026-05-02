from supermarioworld.scenes_component import EmptyScene, GameType
from supermarioworld.johnson import Johnson

import random



class Test(EmptyScene):
    def __init__(self, game: GameType):
        super().__init__(game)

        self.shader = CustomShader(game, shader_filename="test.frag")
        self.text = TextRender(game)
        self.text.SpaceX = 25
        self.text.Zayer = 2
        
        self.text_2 = TextRender(game)
        self.text_2.SpaceX = 35
        self.text_2.Zayer = 2

        self.sprite = SpriteRender(game=game)
        

        self.time = 300


    def onUpdate(self):
        self.time -= self.game.delta_time

    def onEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.game.request.redirectScene("menu")


    def onRender(self):
        self.text.renderText(f"{int(self.game.getFps())}")
        self.sprite.renderSprite()

        
        
    
    def onSave(self):
        print("Hello")




class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)
        #MUSIC
        pg.mixer_music.load(game.paths.SoundtrackPath("music/title-name.mp3"))
        pg.mixer_music.play(-1, fade_ms=2000)

        self.sound_choose = pg.mixer.Sound(game.paths.SoundtrackPath("sounds/map.wav"))
        self.sound_cancer = pg.mixer.Sound(game.paths.SoundtrackPath("sounds/pause.wav"))
        self.sound_pointer = pg.mixer.Sound(game.paths.SoundtrackPath("sounds/pointer.mp3"))

        #JSON DATAS
        self.account_0 = Johnson(game.paths.DataPath("player-info/player0.json")).readData()
        self.account_1 = Johnson(game.paths.DataPath("player-info/player1.json")).readData()
        self.account_2 = Johnson(game.paths.DataPath("player-info/player2.json")).readData()
        self.account_dict = {f"P-{i}": f"player-info/player{i}" for i in range(3)}

        #ATTRIBUTES
        self.timer_appear = 0
        self.timer_dissappear = 1
        self.x_1, self.x_2 = 0, self.game.width

        self.r = random.uniform(0.0, 0.5)
        self.g = random.uniform(0.1, 0.7)
        self.b = random.uniform(0.4, 0.8)


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


        #GRAPHICS
        self.fade = FadeEffect(game)
        self.fade.Alpha = 1.0
        
        self.shader = CustomShader(game, "menu.frag")

        self.title = SpriteRender(game, self.shader)
        self.title_border = SpriteRender(game)
        self.background = SpriteRender(game)


        self.text_1 = TextRender(game)
        self.text_1.Position = glm.vec2(self.game.width // 2 - 315 // 2, self.game.height // 2 - 60)
        self.text_1.SpaceX = 35
      

        self.text_2 = TextRender(game)
        self.text_2.Position = glm.vec2(self.game.width // 2 - 315 // 2, self.game.height // 2 + 20)
        self.text_2.StartX = 15
        self.text_2.SpaceX = 35
  
        
        self.text_3 = TextRender(game)
        self.text_3.Position = glm.vec2(self.game.width // 2 - 315 // 2, self.game.height // 2 + 100)
        self.text_3.StartX = 65
        self.text_3.SpaceX = 35
        

        self.text_4 = TextRender(game)
        self.text_4.Position = glm.vec2(self.game.width // 2 - 515 // 2, self.game.height // 2 - 80)
        self.text_4.StartX = 30
        self.text_4.SpaceX = 35
       

        self.text_5 = TextRender(game)
        self.text_5.Position = glm.vec2(self.game.width // 2 - 515 // 2, self.game.height // 2)
        self.text_5.StartX = 30
        self.text_5.SpaceX = 35
        

        self.text_6 = TextRender(game)
        self.text_6.Position = glm.vec2(self.game.width // 2 - 515 // 2, self.game.height // 2 + 80)
        self.text_6.StartX = 30
        self.text_6.SpaceX = 35
        

        self.text_7 = TextRender(game)
        self.text_7.Position = glm.vec2(self.game.width // 2 - 515 // 2, self.game.height // 2 - 180)
        self.text_7.Scale = glm.vec2(20)
        self.text_7.StartX = 10
        self.text_7.SpaceX = 25

        self.title.Texture = load_texture(game, game.paths.AssetPath("menu/title.png"))
        self.title.Position = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 250)
        self.title.Scale = glm.vec2(376, 112)
        self.title.Zayer = 1

        self.title_border.Texture = load_texture(game, game.paths.AssetPath("menu/title-border.png"))
        self.title_border.Position = glm.vec2(0, 0)
        self.title_border.Scale = glm.vec2(self.game.width, self.game.height)
        self.title_border.Zayer = 2

        self.background.Texture = load_texture(game, game.paths.AssetPath("menu/background.png"))
        self.background.Scale = glm.vec2(self.game.width, self.game.height)
        self.background.Zayer = 0




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
            self.fade.fadeOut(0.7)
            pg.mixer_music.fadeout(2500)

            
            self.switch_timer += self.game.delta_time

            if self.switch_timer >= self.switch_delay and self.switch_target_scene:
                self.game.request.redirectScene(self.switch_target_scene)

        else:
            self.fade.fadeIn(2)


        
            
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
                    self.game.data_settings_read["current-player-account-path"] = self.account_dict[self.options[self.selected]]
                    self.switching = True
                    self.switch_timer = 0
                    self.switch_target_scene = "cutscene"

   
            if event.key == pg.K_z and self.switching_game:
                self.sound_cancer.play()
                self.switching_game = False
                self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
                self.selected = 0

        
            
        
    
    def onRender(self):
        self.game.setColorScreen(self.r, self.g, self.b)

        self.background.Position = glm.vec2(self.x_1, glm.sin(self.x_1 * 0.2))
        self.background.renderSprite()

        self.background.Position = glm.vec2(self.x_2, glm.sin(self.x_1 * 0.2))
        self.background.renderSprite()

        if not self.switching_game:
            self.shader.setColor = glm.vec3(1)
            self.title.Position = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 250)
            self.title.renderSprite()
            

            self.shader.setColor = glm.vec3(0)
            self.title.Position = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 240)
            self.title.renderSprite()
            

            self.text_1.renderText("PLAY-MODE")
            self.text_2.renderText("SETTINGS")
            self.text_3.renderText("QUIT")
        else:
            self.text_4.renderText(f"PLAYER-0 - {self.account_0['passed-level-count']}")
            self.text_5.renderText(f"PLAYER-1 - {self.account_1['passed-level-count']}")
            self.text_6.renderText(f"PLAYER-2 - {self.account_2['passed-level-count']}")
            self.text_7.renderText("xCHOOSE THE PLAYERx")

        self.title_border.renderSprite()
        self.fade.renderFadeEffect()

       
    


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
