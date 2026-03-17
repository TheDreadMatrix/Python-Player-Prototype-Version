from MyGame.scenes_component import EmptyScene




class Level(EmptyScene):
    def __init__(self, game, biome: str, music_name: str):
        super().__init__(game)

    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        return super().onRender()
    

    def onSave(self):
        return super().onSave()




class Tutorial(EmptyScene):
    def __init__(self, game):
        super().__init__(game)

    def onUpdate(self):
        return super().onUpdate()


    def onEvent(self, event):
        return super().onEvent(event)


    def onRender(self):
        return super().onRender()
    