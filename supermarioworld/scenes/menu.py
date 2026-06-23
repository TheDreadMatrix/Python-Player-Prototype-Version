from supermarioworld.scenes.base import EmptyScene


from supermarioworld.rendering.users import TextLabel, FadeLabel
from supermarioworld.rendering.shaders import CustomShader




import pygame as pg
import math






  


class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)
   

        #MUSIC
        self.audio.load("title")
        self.audio.play(loop=True)

        
        self.sound_choose = game.audio.giveSound("choose")
        self.sound_cancer = game.audio.giveSound("pause")
        self.sound_pointer = game.audio.giveSound("pointer")

    
        
        # Account
        self.accounts = {"P-0": 0, "P-1": 1, "P-2": 2}


        # Alpha fading and some redirecting
        self.timer = 0

        self.our_y = -100
        self.x_1, self.x_2 = 0, self.game.width

        self.fade_label = FadeLabel(game)
        self.fade_label.fadeIn(speed=0.6)

        
        self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
        self.selected = 0

        self.switch_timer = 0
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

        

        # Pixel mosaic
        self.pixel_size = 1
        self.target_pixel_size = 1
        self.pixel_speed = 60

        self.renderer.createFbo("background", (game.width, game.height))


        self.pixel_mosiac_shader = CustomShader(game, "testing/default.vert", "post-processing/post-processing-pxm.frag")
        self.pixel_mosiac_shader.defineUniform("pixel_size", "pixelSize")
        self.pixel_mosiac_shader.defineUniform("texture_size", "textureSize")

        self.renderer.regShader("pxm", self.pixel_mosiac_shader)

        

        self.text_play = TextLabel(game,  text=self.locale.gettext("menu-play"), size_font=32, font_key="pixel")
        self.text_play.position = (game.width // 2 - self.text_play.size[0] // 2 - 10, 250)
        

        self.text_options = TextLabel(game,  text=self.locale.gettext("menu-options"), size_font=32, font_key="pixel")
        self.text_options.position = (game.width // 2 - self.text_options.size[0] // 2 - 10, 350)
       

        self.text_quit = TextLabel(game,  self.locale.gettext("menu-quit"), size_font=32, font_key="pixel")
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
        self.fade_label.update() 
       

        # moving background
        self.our_y = math.sin(self.timer) * 10
      

        self.x_1 += 36 * self.game.delta_time
        self.x_2 += 36 * self.game.delta_time

        if self.x_1 >= self.game.width:
            self.x_1 = self.x_2 - self.game.width

        if self.x_2 >= self.game.width:
            self.x_2 = self.x_1 - self.game.width

    
        # pixel
        if self.switching:
            self.target_pixel_size = 128
        else:
            self.target_pixel_size = 1

        

        if self.pixel_size < self.target_pixel_size:
            self.pixel_size += self.pixel_speed * self.game.delta_time
            self.pixel_size = min(self.pixel_size, self.target_pixel_size)

        elif self.pixel_size > self.target_pixel_size:
            self.pixel_size -= self.pixel_speed * self.game.delta_time
            self.pixel_size = max(self.pixel_size, self.target_pixel_size)


        # fade effect
        if self.switching:
            self.switch_timer += self.game.delta_time

            if self.switch_timer >= 2.5 and self.switch_target_scene:
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
                        self.switch_target_scene = "base:settings" if selected_option == "SETTINGS" else "base:quit"

                        self.audio.fadeOut(2500)
                        self.fade_label.fadeOut(speed=0.6)

                else:
                    self.account.loadPlayer(self.accounts.get(self.options[self.selected], 0))
                    
                    self.switching = True
                    self.switch_timer = 0
                    self.switch_target_scene = f"base:{self.game.player.current_overworld}"

                    self.audio.fadeOut(3000)
                    self.fade_label.fadeOut(speed=0.6)

   
            if event.key == pg.K_z and self.switching_game:
                self.sound_cancer.play()
                self.switching_game = False
                self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
                self.selected = 0

        
            
        
    
    def onRender(self):
        self.renderer.beginFbo("background")
        self.game.clearColor(0.53, 0.99, 1)
        
        

        self.renderer.render("background", size=(self.game.width, self.game.height), position=(self.x_1, self.our_y))
        self.renderer.render("background", size=(self.game.width, self.game.height), position=(self.x_2, self.our_y))

        for texture_key, instances in self.batches.items():
            self.renderer.renderInstance(texture_key, instances=instances)


        self.renderer.endFbo()

        self.pixel_mosiac_shader.setUniformByOneTime("pixel_size", self.pixel_size)
        self.pixel_mosiac_shader.setUniformByOneTime("texture_size", (self.game.width, self.game.height))

        self.renderer.renderFbo("background", size=(self.game.width, self.game.height), shader_key="pxm")

        self.renderer.render("title-border", size=(self.game.width, self.game.height))


        
        self.renderer.render("title", size=(360, 160), position=(self.game.width // 2 - 180, 70), r=0, g=0, b=0, a=0.7)
        self.renderer.render("title", size=(360, 160), position=(self.game.width // 2 - 180, 60))

        

        self.text_play.render()
        self.text_options.render()  
        self.text_quit.render()


        self.fade_label.render()

        
       
    def onSave(self):
        self.renderer.deleteFbo("background")
        self.renderer.delShader("pxm")
        
        self.text_quit.delRes()
        self.text_options.delRes()
        self.text_play.delRes()
  

        self.game.assets.delImage("title")
        self.game.assets.delImage("title-border")
        self.game.assets.delImage("background")
        self.game.assets.delImage("b1")
        self.game.assets.delImage("b4")
        

        
       
    

class QuitScene(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        self.request.closeGame()