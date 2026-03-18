from MyGame.scenes_component import EmptyScene
from MyGame.anotation import GameType
from MyGame.johnson import Johnson, readShader, getAD
from MyGame.requirements import pg, mgl, glm
from MyGame.utilits.textures.texture import create_texture
from MyGame.utilits.atlas import FontAtlas



class Test(EmptyScene):
    def __init__(self, game: GameType):
        super().__init__(game)
        self.text_atlas = FontAtlas()

        
        self.ivbo = self.game.ctx.buffer(reserve=4096)
        self.ivbo.write(self.text_atlas.generateTextListByte(f"{self.game.getFps()}", space_x=50, space_y=75))


        


        self.atlas = create_texture(self.game.ctx, getAD("atlas/fonts.png"), flip_y=False)

        self.program = self.game.ctx.program(readShader("text/shader.vert"), readShader("text/shader.frag"))
        self.vao = self.game.ctx.vertex_array(self.program, [(self.game.vbo, "2f 2f", "inPos", "inUV"), (self.ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=self.game.ebo)

        self.timer = 0



    def onUpdate(self):
        self.ivbo.write(self.text_atlas.generateTextListByte(f"{self.game.getFps():.2f}", space_x=50, space_y=75))
        self.timer += self.game.delta_time

        if self.timer >= 3.5:
            pass

    def onEvent(self, event):
        pass


    def onRender(self):
        self.game.ctx.clear(0, 1, 0, 1)

        self.atlas.use()

        self.program["unPos"] = glm.vec2(0, 100)
        self.program["unScale"] = glm.vec2(50, 50)
        self.program["unAtlas"] = glm.vec2(8, 8)
        self.program["unZayer"] = 1
        self.program["color_change"] = glm.vec3(248/255, 216/255, 112/255)
        self.program["tex"] = 0
        self.vao.render(mgl.TRIANGLES, instances=self.text_atlas.instance_count)
    




class Menu(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

        self.atlas_text = FontAtlas()

        #TEXTURES
        self.text_atlas_texture = create_texture(self.game.ctx, getAD("atlas/fonts.png"), flip_y=False)
        self.title = create_texture(self.game.ctx, getAD("title.png"), flip_y=False)
        self.title_border = create_texture(self.game.ctx, getAD("title-border.png"), flip_y=False)

        #BUFFERS
    
        self.ivbo = self.game.ctx.buffer(reserve=1024)
        self.ivbo.write(self.atlas_text.generateTextListByte("PLAY MODE\nSETTINGS\nQUITc", space_x=25, space_y=100, 
                                                             start_x=self.game.width // 2 - 100, 
                                                             start_y=self.game.height // 2 - 150))


        self.program_text = self.game.ctx.program(readShader("text/shader.vert"), readShader("text/shader.frag"))
        self.vao_text = self.game.ctx.vertex_array(self.program_text, [(self.game.vbo, "2f 2f", "inPos", "inUV"), (self.ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=self.game.ebo)

        self.program = self.game.ctx.program(readShader("textures/shader.vert"), readShader("textures/shader.frag"))
        self.vao = self.game.ctx.vertex_array(self.program, [(self.game.vbo, "2f 2f", "inPos", "inUV")], index_buffer=self.game.ebo)



    def onUpdate(self):
        pass
    
    def onEvent(self, event):
        if event.type == pg.VIDEORESIZE:
            self.ivbo.write(self.atlas_text.generateTextListByte("PLAY-MODE\nSETTINGS\nQUITc", space_x=50, space_y=135))
    
    def onRender(self):
        self.game.ctx.clear(0, 1, 0, 1, depth=1.0)

        self.title.use()

        self.program["unPos"] = glm.vec2(self.game.width // 2 - 186, self.game.height // 2 - 250)
        self.program["unScale"] = glm.vec2(366, 112)
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

        self.title_border.use()

        self.program["unPos"] = glm.vec2(0, 0)
        self.program["unScale"] = glm.vec2(self.game.width, self.game.height)
        self.program["unZayer"] = 2
        self.program["color_change"] = glm.vec3(0.9, 0.3, 0.6)
        self.program["tex"] = 0
        self.vao.render(mgl.TRIANGLES)


        self.text_atlas_texture.use()
        self.program_text["unPos"] = glm.vec2(0, 100)
        self.program_text["unScale"] = glm.vec2(25, 25)
        self.program_text["unAtlas"] = glm.vec2(8, 8)
        self.program_text["unZayer"] = 1
        self.program_text["color_change"] = glm.vec3(0.9, 0.3, 0.6)
        self.program_text["tex"] = 0
        self.vao_text.render(mgl.TRIANGLES, instances=self.atlas_text.instance_count)

    
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
        pass
    
    def onSave(self):
        pass