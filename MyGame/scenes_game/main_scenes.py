from MyGame.scenes_component import EmptyScene
from MyGame.anotation import GameType
from MyGame.johnson import Johnson, readShader, getAD
from MyGame.requirements import pg, mgl, glm
from MyGame.utilits.textures.texture import create_texture
from MyGame.rendering import TextRender



class Test(EmptyScene):
    def __init__(self, game: GameType):
        super().__init__(game)
       

        
        self.ivbo = self.game.ctx.buffer(reserve=4096)
        

        self.program = self.game.programs.shader_text
        self.vao = self.game.ctx.vertex_array(self.program, [(self.game.vbo, "2f 2f", "inPos", "inUV"), (self.ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=self.game.ebo)

        self.timer = 0



    def onUpdate(self):
    
        self.timer += self.game.delta_time

        if self.timer >= 3.5:
            pass

    def onEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_l:
                self.game.switchScene("menu")


    def onRender(self):
        self.game.ctx.clear(0, 1, 0, 1)


        self.program["unPos"] = glm.vec2(0, 100)
        self.program["unScale"] = glm.vec2(50, 50)
        self.program["unAtlas"] = glm.vec2(8, 8)
        self.program["unZayer"] = 1
        self.program["color_change"] = glm.vec3(248/255, 216/255, 112/255)
        self.program["tex"] = 0
        self.vao.render(mgl.TRIANGLES)
    




class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        #ATTRIBUTES
        self.timer_appear = 0
        self.timer_dissappear = 1


        self.alpha = 0
        self.options = ["PLAY MODE", "SETTINGS", "QUIT"]
        self.selected = 0

        self.active = glm.vec3(1, 1, 0)   
        self.inactive = glm.vec3(1, 1, 1)

        self.switch_timer = 0
        self.switching = False


        #GRAPHICS
        self.title = create_texture(self.game.ctx, getAD("title.png"), flip_y=False)
        self.title_border = create_texture(self.game.ctx, getAD("title-border.png"), flip_y=False)


        self.text_1 = TextRender(game)
        self.text_1.Position = glm.vec2(self.game.width // 2 - 315 // 2, self.game.height // 2 - 60)
        self.text_1.Scale = glm.vec2(25)
        self.text_1.SpaceX = 35
        self.text_1.Alpha = self.alpha

        self.text_2 = TextRender(game)
        self.text_2.Position = glm.vec2(self.game.width // 2 - 315 // 2, self.game.height // 2 + 20)
        self.text_2.Scale = glm.vec2(25)
        self.text_2.StartX = 15
        self.text_2.SpaceX = 35
        self.text_2.Alpha = self.alpha
        
        self.text_3 = TextRender(game)
        self.text_3.Position = glm.vec2(self.game.width // 2 - 315 // 2, self.game.height // 2 + 100)
        self.text_3.Scale = glm.vec2(25)
        self.text_3.StartX = 65
        self.text_3.SpaceX = 35
        self.text_3.Alpha = self.alpha


        self.program = self.game.programs.shader_textures
        self.vao = self.game.ctx.vertex_array(self.program, [(self.game.vbo, "2f 2f", "inPos", "inUV")], index_buffer=self.game.ebo)




    def onUpdate(self):
        if self.alpha != 1:
            self.timer_appear += self.game.delta_time * 0.6
            self.alpha = glm.clamp(0, self.timer_appear, 1)

        if self.switching:
            self.timer_dissappear -= self.game.delta_time * 0.3
            self.alpha = glm.clamp(self.timer_dissappear, 0.0, 1.0)

            if self.switching and (self.options[self.selected] == "SETTINGS" or self.options[self.selected] == "QUIT"):
                self.switch_timer += self.game.delta_time

                if self.switch_timer >= 3.9: 
                    mode = self.options[self.selected]
                    if mode == "SETTINGS":
                        self.game.switchScene("settings")

                    elif mode == "QUIT":
                        self.game.switchScene("quit")


        self.text_1.Alpha = self.alpha
        self.text_2.Alpha = self.alpha
        self.text_3.Alpha = self.alpha

        self.text_1.ColorChange = self.active if self.selected == 0 else self.inactive
        self.text_2.ColorChange = self.active if self.selected == 1 else self.inactive
        self.text_3.ColorChange = self.active if self.selected == 2 else self.inactive


        
            
    def onEvent(self, event):
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
                self.switching = True
        
    
    def onRender(self):
        self.game.ctx.clear(0, 0, 0)

        self.title.use()

        self.program["unPos"] = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 250)
        self.program["unScale"] = glm.vec2(376, 112)
        self.program["unZayer"] = 1
        self.program["color_change"] = glm.vec3(1, 1, 1)
        self.program["tex"] = 0
        self.program["alpha"] = self.alpha 
        self.vao.render(mgl.TRIANGLES)

        self.program["unPos"] = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 240)
        self.program["unScale"] = glm.vec2(366, 112)
        self.program["unZayer"] = 0
        self.program["color_change"] = glm.vec3(0, 0, 0)
        self.program["tex"] = 0
        self.program["alpha"] = self.alpha
        self.vao.render(mgl.TRIANGLES)

        self.title_border.use()

        self.program["unPos"] = glm.vec2(0, 0)
        self.program["unScale"] = glm.vec2(self.game.width, self.game.height)
        self.program["unZayer"] = 2
        self.program["color_change"] = glm.vec3(1)
        self.program["tex"] = 0
        self.program["alpha"] = self.alpha
        self.vao.render(mgl.TRIANGLES)

        self.text_1.renderText("PLAY MODE")
        self.text_2.renderText("SETTINGS")
        self.text_3.renderText("QUIT")

    
    def onSave(self):
        pass
    


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