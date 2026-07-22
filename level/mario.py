from supermarioworld.enums.controllers import Keys
from supermarioworld.enums.state import CharacterPowerup, CharacterEnvironment, CharacterStarup, CharacterAction

from supermarioworld.rendering.animation import AnimationCutOut

from level.entities import Character
import random



class Mario(Character):
    def __init__(self, game, world):
        super().__init__(game=game)
        self.world = world

        game.assets.regAtlas("mario-spr", "atlas/mario.png")

        self.w, self.h = 48, 72
        self.x = 120
        self.y = 440

        self.flip_x = True
        self.looking = False
        self.ducking = False
        self.spin_jump = False
        self.skidding = False
        self.run_jump = False

        self.walk_speed = 220
        self.run_speed = 400

        self.p_speed = 0.0
        self.max_p_speed = 1.0

        self.acceleration = 1200

        # Attributes
        self.power = CharacterPowerup.SMALL
        self.environment = CharacterEnvironment.GROUND
        self.action = CharacterAction.IDLE
        self.star_state = CharacterStarup.NORMAL


        # Animations
        self.animations = {
            (CharacterPowerup.SMALL, CharacterAction.IDLE): AnimationCutOut(game, key_atlas="mario-spr", frames=[(24, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.WALK): AnimationCutOut(game, key_atlas="mario-spr", frames=[(24, 48, 16, 24), (232, 49, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.LOOK_UP): AnimationCutOut(game, key_atlas="mario-spr", frames=[(76, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.DUCK): AnimationCutOut(game, key_atlas="mario-spr", frames=[(128, 56, 16, 16)]),
            (CharacterPowerup.SMALL, CharacterAction.FALL): AnimationCutOut(game, key_atlas="mario-spr", frames=[(128, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.JUMP): AnimationCutOut(game, key_atlas="mario-spr", frames=[(76, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.SKID): AnimationCutOut(game, key_atlas="mario-spr", frames=[(700, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.RUN_JUMP): AnimationCutOut(game, key_atlas="mario-spr", frames=[(180, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.RUN): AnimationCutOut(game, key_atlas="mario-spr", frames=[(336, 49, 16, 24), (440, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.SPIN): AnimationCutOut(game, key_atlas="mario-spr", frames=[(232, 112, 16, 24), (284, 112, 16, 24), (336, 112,16, 24), (388, 112, 16, 24)], durations=[0.05, 0.05, 0.05, 0.05]),
        }


    def set_height(self, new_h):
        if new_h == self.h:
            return

        bottom = self.y + self.h
        self.h = new_h
        self.y = bottom - self.h

    def can_stand(self):
        test_y = self.y - (72 - self.h)

        for block in self.world.objects:
            if (
                self.x < block.x + block.w and
                self.x + self.w > block.x and
                test_y < block.y + block.h and
                test_y + 72 > block.y
            ):
                return False

        return True


    def update_action(self):
        if self.ducking:
            self.action = CharacterAction.DUCK
        
        elif self.looking:
            self.action = CharacterAction.LOOK_UP
        
        
        elif self.spin_jump:
            self.action = CharacterAction.SPIN
        
        elif self.vy != 0:
            if self.run_jump:
                self.action = CharacterAction.RUN_JUMP
        
            elif self.vy > 0:
                self.action = CharacterAction.FALL 
            else:
                self.action = CharacterAction.JUMP
        
        elif self.skidding:
            self.action = CharacterAction.SKID
        
        elif self.vx != 0:
            if self.p_speed >= 1.0:
                self.action = CharacterAction.RUN
            else:
                self.action = CharacterAction.WALK
        else:
            self.action = CharacterAction.IDLE


    def update(self, delta_time):
        move = 0

        self.update_action()


        # X moving
        if self.keyboard.isPressed(Keys.D):
            move = 1
            self.flip_x = True
        elif self.keyboard.isPressed(Keys.A):
            move = -1
            self.flip_x = False

        self.skidding = (self.on_ground and move != 0 and self.vx != 0 and move != (1 if self.vx > 0 else -1))
        
        running = self.keyboard.isPressed(Keys.X)
        fast = abs(self.vx) > self.walk_speed * 0.9

        if running and fast and self.on_ground:
            self.p_speed = min(self.max_p_speed, self.p_speed + delta_time * 1.1)
        else:
            self.p_speed = max(0, self.p_speed - delta_time * 3)

        target_speed = move * (self.walk_speed if not running else self.run_speed) 

        if self.vx < target_speed:
            self.vx = min(self.vx + self.acceleration * delta_time, target_speed)

        elif self.vx > target_speed:
            self.vx = max(self.vx - self.acceleration * delta_time, target_speed)

        
                    

        # Cascade
        if self.keyboard.isPressed(Keys.W):
            self.looking = True
            self.vx = 0
        else:
            self.looking = False

        if self.keyboard.isPressed(Keys.S):
            self.ducking = True
            self.vx = 0
    
            self.set_height(48)
        else:
            self.ducking = False
            if self.can_stand():
                self.set_height(72)


        # Y moving
        if self.keyboard.isPressed(Keys.SPACE) and self.on_ground:
            self.run_jump = self.p_speed >= 1.0
            self.vy = -800


        elif self.keyboard.isPressed(Keys.Z) and self.on_ground:
            self.flip_x = random.choice([True, False])
            self.spin_jump = True
            self.vy = -500




        super().update(delta_time)


    def move_x(self, dt):
        self.x += self.vx * dt

        for block in self.world.objects:
            if self.intersects(block):

                if self.vx > 0:
                    self.x = block.x - self.w

                elif self.vx < 0:
                    self.x = block.x + block.w

    def move_y(self, dt):
        self.vy += self.gravity * dt
        self.y += self.vy * dt

        self.on_ground = False
        

        for block in self.world.objects:
            if self.intersects(block):

                if self.vy > 0:
                    self.y = block.y - self.h
                    self.vy = 0
                    self.on_ground = True
                    self.run_jump = False
                    self.spin_jump = False

                elif self.vy < 0:
                    self.y = block.y + block.h
                    self.vy = 0


    def render(self, camera):
        animation = self.animations.get((self.power, self.action))

        animation.update()

        x, y = camera.apply(self.x, self.y)

    
        self.renderer.render(animation.getTextureKey(), position=(x, y), size=(self.w, self.h), flx=self.flip_x)


