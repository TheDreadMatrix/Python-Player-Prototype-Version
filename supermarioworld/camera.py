
class BaseCameraMode:
    def update(self, camera: "Camera", delta_time: float, **kwargs): pass



class FollowMode(BaseCameraMode):
    
    def update(self, camera, delta_time, **kwargs):
        target_x = kwargs["target_x"]
        target_y = kwargs["target_y"]

        target_x -= camera.screen_width / 2
        target_y -= camera.screen_height / 2

        camera.x += (target_x - camera.x) * camera.smooth
        camera.y += (target_y - camera.y) * camera.smooth

        camera.x = max(camera.bound_left, min(camera.x, camera.bound_right - camera.screen_width))

        camera.y = max(camera.bound_top, min(camera.y, camera.bound_bottom - camera.screen_height))


class AutoMode(BaseCameraMode):
    def __init__(self, speed_x=200, speed_y=200):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, camera, delta_time, **kwargs):
        camera.x += self.speed_x * delta_time
        camera.y += self.speed_y * delta_time




class Camera:
    def __init__(self, screen_width: int, screen_height: int, camera_mode=FollowMode(), smooth: float = 0.1):
        self.camera_mode = camera_mode

        self.x = 0
        self.y = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.smooth = smooth

        self.bound_left = 0
        self.bound_top = 0
        self.bound_right = 0
        self.bound_bottom = 0

    def setMode(self, mode: BaseCameraMode):
        self.camera_mode = mode

    def setBounds(self, left: float, top: float, right: float, bottom: float):
        self.bound_left = left
        self.bound_top = top
        self.bound_right = right
        self.bound_bottom = bottom

    def update(self, delta_time: float, **kwargs):
        self.camera_mode.update(self, delta_time, **kwargs)
        

    def apply(self, x: float, y: float):
        return (x - self.x, y - self.y)




