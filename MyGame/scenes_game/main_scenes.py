from MyGame.scenes_component import EmptyScene
from MyGame.anotation import GameType
from MyGame.johnson import Johnson, readShader, getAD, getDD
from MyGame.requirements import pg, mgl, glm
from MyGame.utilits.textures.texture import create_texture
from MyGame.rendering import TextRender



class Test(EmptyScene):
    def __init__(self, game: GameType):
        super().__init__(game)

        
        



    def onUpdate(self):
        pass

    def onEvent(self, event):
        pass


    def onRender(self):
        pass
    
    def onSave(self):
        print("Hello")




class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)
        #JSON DATAS
        self.account_0 = Johnson(getDD("player-info/player0.json")).readData()
        self.account_1 = Johnson(getDD("player-info/player1.json")).readData()
        self.account_2 = Johnson(getDD("player-info/player2.json")).readData()
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
        self.switching = False
        self.switching_game = False


        #GRAPHICS
        self.title = create_texture(self.game.ctx, getAD("title.png"), flip_y=False)
        self.title_border = create_texture(self.game.ctx, getAD("title-border.png"), flip_y=False)
        self.background = create_texture(self.game.ctx, getAD("background.png"), flip_y=False)


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
    


        self.program = self.game.programs.shader_textures
        self.vao = self.game.ctx.vertex_array(self.program, [(self.game.vbo, "2f 2f", "inPos", "inUV")], index_buffer=self.game.ebo)




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

            
            self.switch_timer += self.game.delta_time

            if self.switch_timer >= 2.9: 
                mode = self.options[self.selected]
                if mode == "SETTINGS":
                    self.game.switchScene("settings")

                elif mode == "QUIT":
                    self.game.switchScene("quit")


        if not self.switching_game:
            self.text_1.ColorChange = self.active if self.selected == 0 else self.inactive
            self.text_2.ColorChange = self.active if self.selected == 1 else self.inactive
            self.text_3.ColorChange = self.active if self.selected == 2 else self.inactive
        else:

            self.text_4.ColorChange = self.active if self.selected == 0 else self.inactive
            self.text_5.ColorChange = self.active if self.selected == 1 else self.inactive
            self.text_6.ColorChange = self.active if self.selected == 2 else self.inactive


        
            
    def onEvent(self, event):   
        if self.switching:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.options) - 1 

            elif event.key == pg.K_s:
                self.selected += 1
                if self.selected >= len(self.options):
                    self.selected = 0

            if event.key == pg.K_q:
                if not self.switching_game:
                    selected_option = self.options[self.selected]

                    if selected_option == "PLAY MODE":
                        self.switching_game = True
                        self.options = ["P-0", "P-1", "P-2"]
                        self.selected = 0

                    else:
                        self.switching = True
                        self.switch_timer = 0

                else:
                    self.game.data_settings_read["current-player-account-path"] = self.account_dict[self.options[self.selected]]
                    self.game.switchScene("cutscene")  
                    self.switching = True

   
            if event.key == pg.K_z and self.switching_game:
                self.switching_game = False
                self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
                self.selected = 0

        
            
        
    
    def onRender(self):
        self.game.ctx.clear(0, 0, 0)

        if not self.switching_game:
            self.title.use()

            self.program["unPos"] = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 250)
            self.program["unScale"] = glm.vec2(376, 112)
            self.program["unZayer"] = 1
            self.program["color_change"] = glm.vec3(1, 1, 1)
            self.program["tex"] = 0
            self.vao.render(mgl.TRIANGLES)

            self.program["unPos"] = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 240)
            self.program["unScale"] = glm.vec2(366, 112)
            self.program["unZayer"] = 0
            self.program["color_change"] = glm.vec3(0, 0, 0)
            self.program["tex"] = 0
            self.vao.render(mgl.TRIANGLES)

            self.text_1.renderText("PLAY MODE")
            self.text_2.renderText("SETTINGS")
            self.text_3.renderText("QUIT")
        else:
            self.text_4.renderText(f"PLAYER-0 - {self.account_0["passed-level-count"]}")
            self.text_5.renderText(f"PLAYER-1 - {self.account_1["passed-level-count"]}")
            self.text_6.renderText(f"PLAYER-2 - {self.account_2["passed-level-count"]}")
            self.text_7.renderText("xCHOOSE THE PLAYERx")

        self.title_border.use()

        self.program["unPos"] = glm.vec2(0, 0)
        self.program["unScale"] = glm.vec2(self.game.width, self.game.height)
        self.program["unZayer"] = 2
        self.program["color_change"] = glm.vec3(1)
        self.program["tex"] = 0
        self.vao.render(mgl.TRIANGLES)

        self.background.use()

        self.program["unPos"] = glm.vec2(self.x_1, glm.sin(self.x_1 * 0.1))
        self.program["unScale"] = glm.vec2(self.game.width, self.game.height)
        self.program["unZayer"] = 0
        self.program["color_change"] = glm.vec3(1)
        self.program["tex"] = 0
        self.vao.render(mgl.TRIANGLES)

        self.program["unPos"] = glm.vec2(self.x_2, glm.sin(self.x_1 * 0.1))
        self.program["unScale"] = glm.vec2(self.game.width, self.game.height)
        self.program["unZayer"] = 0
        self.program["color_change"] = glm.vec3(1)
        self.program["tex"] = 0 
        self.vao.render(mgl.TRIANGLES)

       
    


class Settings(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

    def onUpdate(self):
        pass
    
    def onEvent(self, event):
        pass
    
    def onRender(self):
        self.game.ctx.clear(0, 1, 0)
    
    def onSave(self):
        pass