from supermarioworld.scenes.base import EmptyScene



class PlayerStart(EmptyScene):
    def onInitialization(self, game, **kwargs):
        self.assets.regCutOutImage("MARIO", "fonts", x=13, y=344, w=43, h=15)
        self.assets.regCutOutImage("START!", "fonts", x=64, y=344, w=53, h=15)

        self.timer = 0
        self.audio.giveSound("coin").play()

    def onUpdate(self):
        self.timer += self.game.delta_time

        if self.timer >= 0.6:
            self.request.redirectScene(self.game.SCENE_DATA.get("scene", "base:level-1"))


    def onEvent(self, event):
        return super().onEvent(event)


    def onRender(self):
        scale = 4

        mario_w, mario_h = 43 * scale, 15 * scale
        start_w, start_h = 53 * scale, 15 * scale

        gap = 12
        total_w = mario_w + gap + start_w

        x = (self.game.width - total_w) / 2
        y = (self.game.height - mario_h) / 2

        self.renderer.render(
            "MARIO",
            position=(x, y),
            size=(mario_w, mario_h)
        )

        self.renderer.render(
            "START!",
            position=(x + mario_w + gap, y),
            size=(start_w, start_h)
        )



    def onSave(self):
        self.game.SCENE_DATA.clear()
    