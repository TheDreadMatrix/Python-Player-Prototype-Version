from supermarioworld.scenes.base import EmptyScene


from supermarioworld.rendering.users import TextLabel
from supermarioworld.rendering.animation import Animation, AnimationCutOut




import pygame as pg
import glm





  


class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)
   

        #MUSIC
        self.audio.load("title")
        self.audio.setVolume(game.account.getMusicVolume())

        
        self.sound_choose = game.audio.giveSound("choose")
        self.sound_cancer = game.audio.giveSound("pause")
        self.sound_pointer = game.audio.giveSound("pointer")

        
        # Account
        self.accounts = {"P-0": 0, "P-1": 1, "P-2": 2}


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
        game.assets.regImage("title", "menu/title.png")
        game.assets.regImage("title-border", "menu/title-border.png")
        game.assets.regImage("background", "menu/background.png")


        game.assets.regAtlas("blocks", "levels/tile-blocks.png")
        game.assets.regAtlas("koopas", "atlas/koopas.png")
        

        game.assets.regCutOutImage("b1", "blocks", 16, 200, 16, 16)
        game.assets.regCutOutImage("b4", "blocks", 32, 40, 16, 16)

        self.renderer.createFbo("my-fbo", (game.width, game.height))

        self.animation = Animation(game, 
                                   frame_paths=["tests/1.png", "tests/2.png", "tests/3.png"],
                                   durations=[0.1, 0.2, 0.1],
                                   key_images=["m1", "m2", "m3"]
                                   )
        

        self.text_play = TextLabel(game, "text-1", "Play", size_font=32, font_key="pixel")
        self.text_play.position = (game.width // 2 - self.text_play.size[0] // 2 - 10, 250)
        

        self.text_options = TextLabel(game, "text-2", "Options", size_font=32, font_key="pixel")
        self.text_options.position = (game.width // 2 - self.text_options.size[0] // 2 - 10, 350)
       

        self.text_quit = TextLabel(game, "text-3", "Quit", size_font=32, font_key="pixel")
        self.text_quit.position = (game.width // 2 - self.text_quit.size[0] // 2 - 10, 450)
        
        
        
        self.positions = list(range(0, 48 * 50, 48))

        self.batches = {
            "b1": [],
            "b4": []
        }

        # b1
        for position in self.positions:
            self.batches["b1"].append([
                position, 500,
                48, 48,
                0, 0
            ])

        # b4
        for position in self.positions:

            self.batches["b4"].append([
                position, 548,
                48, 48,
                0, 0
            ])

            self.batches["b4"].append([
                position, 596,
                48, 48,
                0, 0
            ])



    
    def onUpdate(self):
        self.timer += self.game.delta_time 
       
        self.animation.update()
        
        self.audio.play(loops=-1, fade_in=2)

        # moving background
        self.our_y = glm.sin(self.timer) * 10
      

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

            self.audio.fadeOut(3)

            
            self.switch_timer += self.game.delta_time

            if self.switch_timer >= self.switch_delay and self.switch_target_scene:
                self.game.request.redirectScene(self.switch_target_scene)



        
            
    def onEvent(self, event):   
        if self.switching:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.request.restartScene()

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
                    self.account.loadPlayer(self.accounts.get(self.options[self.selected], 0))
                    
                    self.switching = True
                    self.switch_timer = 0
                    self.switch_target_scene = "base:cutscene-1"

   
            if event.key == pg.K_z and self.switching_game:
                self.sound_cancer.play()
                self.switching_game = False
                self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
                self.selected = 0

        
            
        
    
    def onRender(self):
        self.game.clearColor(0.53, 0.99, 1)
        
        self.renderer.beginFbo("my-fbo")

        self.renderer.render("background", size=(self.game.width, self.game.height), position=(self.x_1, self.our_y))
        self.renderer.render("background", size=(self.game.width, self.game.height), position=(self.x_2, self.our_y))

        self.renderer.render("title", size=(360, 160), position=(self.game.width // 2 - 180, 70), r=0, g=0, b=0, a=0.7)
        self.renderer.render("title", size=(360, 160), position=(self.game.width // 2 - 180, 60))

        self.renderer.renderQuad(position=(300, 100), r=1, g=0, b=0, mode=1)

        for texture_key, instances in self.batches.items():
            self.renderer.renderInstance(texture_key, instances=instances)

        self.renderer.endFbo()
        self.renderer.renderFbo("my-fbo", size=(self.game.width, self.game.height), r=1, g=1, b=1)

        self.renderer.render("title-border", size=(self.game.width, self.game.height))
        

        self.renderer.render(self.text_play.texture_id, size=self.text_play.size, position=self.text_play.position)
        self.renderer.render(self.text_options.texture_id, size=self.text_options.size, position=self.text_options.position)
        self.renderer.render(self.text_quit.texture_id, size=self.text_quit.size, position=self.text_quit.position)

        
       
    def onSave(self):
        self.renderer.deleteFbo("my-fbo")
        self.animation.delAnimation()

        self.game.assets.delAtlas("blocks")
        self.game.assets.delFont("pixel")

        self.game.assets.delImage("title")
        self.game.assets.delImage("title-border")
        self.game.assets.delImage("background")
        self.game.assets.delImage("b1")
        self.game.assets.delImage("b4")
        

        
       
    

class QuitScene(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        self.request.closeGame()