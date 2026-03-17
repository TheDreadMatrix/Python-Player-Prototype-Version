from MyGame.scenes_component import EmptyScene
from MyGame.anotation import GameType
from MyGame.johnson import Johnson, readShader, getAD
from MyGame.requirements import pg, mgl, glm, array
from MyGame.utilits.texture import create_texture



class Test(EmptyScene):
    def __init__(self, game: GameType):
        super().__init__(game)
        instance_list = [0, 0, 88, 128, 100, 0, 96, 128]

        
        ebo = self.game.ctx.buffer(game.indices)
        vbo = self.game.ctx.buffer(game.vertices)
        ivbo = self.game.ctx.buffer(reserve=4096)
        ivbo.write(array("f", instance_list))


        self.atlas = create_texture(self.game.ctx, getAD("atlas/fonts.png"), flip_y=False)

        self.program = self.game.ctx.program(readShader("text/shader.vert"), readShader("text/shader.frag"))
        self.vao = self.game.ctx.vertex_array(self.program, [(vbo, "2f 2f", "inPos", "inUV"), (ivbo, "2f 2f/i", "inTextPos", "inTextOffset")], index_buffer=ebo)

        self.timer = 0



    def onUpdate(self):
        self.timer += self.game.delta_time

        if self.timer >= 3.5:
            pass

    def onEvent(self, event):
        pass


    def onRender(self):
        self.game.ctx.clear(0, 1, 0, 1)

        self.atlas.use()

        self.program["unPos"] = glm.vec2(100, 100)
        self.program["unScale"] = glm.vec2(100, 100)
        self.program["unAtlas"] = glm.vec2(8, 8)
        self.program["unZayer"] = 1
        self.program["tex"] = 0
        self.vao.render(mgl.TRIANGLES, instances=2)
    




class Menu(EmptyScene):
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