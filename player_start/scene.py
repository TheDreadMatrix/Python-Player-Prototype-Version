from supermarioworld.scenes.base import EmptyScene
from supermarioworld.users import FadeLabel


class PlayerActionScene(EmptyScene):
    def onInitialization(self, game, action="start"):
        self.action = action

        self.fade_label = FadeLabel(game)
        self.fade_label.fadeIn(0.5)
        
        self.redirect = self.game.SCENE_DATA.get("scene", "level-1")

        if action == "start":
            self.max_time = 0.6
            self.audio.giveSound("coin").play()
            self.assets.regCutOutImage("MARIO-START", "fonts", x=13, y=344, w=104, h=15)
        elif action == "bonus-game":
            self.max_time = 0.6
            self.assets.regCutOutImage("BONUS-GAME", "fonts", x=416, y=344, w=81, h=15)
        elif action == "time-up":
            self.max_time = 2.5
            self.redirect = self.game.player.current_overworld
            self.assets.regCutOutImage("TIME", "fonts", x=240, y=344, w=33, h=15)
            self.assets.regCutOutImage("UP", "fonts", x=288, y=344, w=29, h=15)
        elif action == "game-over":
            self.max_time = 13.5
            self.redirect = self.game.player.current_overworld
            self.game.SCENE_DATA["game-over"] = True
            self.audio.giveSound("game-over").play(speed=0.6)
            self.assets.regCutOutImage("GAME", "fonts", x=328, y=344, w=33, h=15)
            self.assets.regCutOutImage("OVER", "fonts", x=376, y=344, w=31, h=15)

        self.scale = 4
        self.gap = 45  
        self.timer = 0

        if action in ("time-up", "game-over"):
            self.left_x = -200
            self.right_x = game.width + 200

            self.speed = 800 
    
    

    def onUpdate(self):
        dt = self.game.delta_time
        self.timer += dt

        self.fade_label.update()

        if self.action in ("time-up", "game-over"):
            left_w = 33 * self.scale

            center = self.game.width / 2

            target_left = center - self.gap / 2 - left_w
            target_right = center + self.gap / 2

            self.left_x = min(self.left_x + self.speed * dt, target_left)

            self.right_x = max(self.right_x - self.speed * dt, target_right)

        if self.timer >= self.max_time:
            self.game.router.redirect(self.redirect)

    def onRender(self):

        if self.action == "start":
            w = 104 * self.scale
            h = 15 * self.scale

            x = (self.game.width - w) / 2
            y = (self.game.height - h) / 2

            self.renderer.render(
                "MARIO-START",
                position=(x, y),
                size=(w, h)
            )

        elif self.action == "bonus-game":
            w = 81 * self.scale
            h = 15 * self.scale

            x = (self.game.width - w) / 2
            y = (self.game.height - h) / 2

            self.renderer.render(
                "BONUS-GAME",
                position=(x, y),
                size=(w, h)
            )

        elif self.action == "time-up":
            h = 15 * self.scale
            y = (self.game.height - h) / 2

            self.renderer.render(
                "TIME",
                position=(self.left_x, y),
                size=(33 * self.scale, h)
            )

            self.renderer.render(
                "UP",
                position=(self.right_x, y),
                size=(29 * self.scale, h)
            )

        elif self.action == "game-over":
            h = 15 * self.scale
            y = (self.game.height - h) / 2

            self.renderer.render(
                "GAME",
                position=(self.left_x, y),
                size=(33 * self.scale, h)
            )

            self.renderer.render(
                "OVER",
                position=(self.right_x, y),
                size=(31 * self.scale, h)
            )

            self.fade_label.render()


    def onSave(self):
        self.game.SCENE_DATA.clear()
    