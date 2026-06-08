import math

class Camera:
    def __init__(self, game, screen_width: int, screen_height: int, smooth: float = 0.1, x: float = 0.0, y: float = 0.0):
        self.game = game

        self.x = x
        self.y = y

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.smooth = smooth

        self.bound_left = 0
        self.bound_top = 0
        self.bound_right = 0
        self.bound_bottom = 0

    def setBounds(self, left: float, top: float, right: float, bottom: float):
        self.bound_left = left
        self.bound_top = top
        self.bound_right = right
        self.bound_bottom = bottom

    def follow(self, target_x: float, target_y: float):
        target_cam_x = target_x - self.screen_width / 2
        target_cam_y = target_y - self.screen_height / 2

        alpha = 1 - math.exp(-self.smooth * self.game.delta_time)
        self.x += (target_cam_x - self.x) * alpha
        self.y += (target_cam_y - self.y) * alpha

        self.x = max(
            self.bound_left,
            min(
                self.x,
                self.bound_right - self.screen_width
            )
        )

        self.y = max(
            self.bound_top,
            min(
                self.y,
                self.bound_bottom - self.screen_height
            )
        )

    def apply(self, x: float, y: float):
        return (x - self.x, y - self.y)

