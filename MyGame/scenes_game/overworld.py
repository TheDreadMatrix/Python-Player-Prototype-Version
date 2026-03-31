from MyGame.scenes_component import EmptyScene




class OverWorld(EmptyScene):
    def __init__(self, game, biome: str, music_name: str):
        super().__init__(game)


    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        self.game._ctx.clear(0, 0, 1)
    

    def onSave(self):
        return super().onSave()
    