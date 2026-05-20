from supermarioworld.package_scenes import EmptyScene




class OverWorld(EmptyScene):
    def __init__(self, game, biome: str, music_name: str):
        super().__init__(game)

        self.audio.load("daemon")

        self.audio.setVolume(self.game.settings_read["music"])

        self.audio.play(loops=-1, fade_in=4)



    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        self.game.clearColor(0, 0, 0)
    

    def onSave(self):
        return super().onSave()
    