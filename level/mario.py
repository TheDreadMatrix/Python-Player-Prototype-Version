from supermarioworld.enums.controllers import Keys
from supermarioworld.enums.state import CharacterPowerup, CharacterEnvironment, CharacterStarup, CharacterAction
from supermarioworld.enums.render import RenderMode


from supermarioworld.rendering.animation import AnimationCutOut

from level.entities import Character
from level.effects import SkidDust
import random



class Mario(Character):
    def __init__(self, world):
        super().__init__(world=world)
        game = self.game
        self.assets.regAtlas("mario-spr", "atlas/mario.png")

        self.w, self.h = 48, 72
        self.x = 120
        self.y = 440

        self.flip_x = True
        self.looking = False
        self.ducking = False
        self.spin_jump = False
        self.was_skidding = False
        self.skidding = False
        self.run_jump = False

    
        self.walk_speed = 220
        self.run_speed = 400

        self.p_speed = 0.0
        self.max_p_speed = 1.0

        

        # Attributes
        self.power = CharacterPowerup.SMALL
        self.environment = CharacterEnvironment.GROUND
        self.action = CharacterAction.IDLE
        self.star_state = CharacterStarup.NORMAL


        # Animations
        self.animations = {
            # Dead
            (CharacterPowerup.SMALL, CharacterAction.DEAD): AnimationCutOut(game, key_atlas="mario-spr", frames=[(544, 266, 16, 24)]),

            # Small
            (CharacterPowerup.SMALL, CharacterAction.IDLE): AnimationCutOut(game, key_atlas="mario-spr", frames=[(24, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.WALK): AnimationCutOut(game, key_atlas="mario-spr", frames=[(24, 48, 16, 24), (232, 49, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.LOOK_UP): AnimationCutOut(game, key_atlas="mario-spr", frames=[(76, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.DUCK): AnimationCutOut(game, key_atlas="mario-spr", frames=[(128, 56, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.FALL): AnimationCutOut(game, key_atlas="mario-spr", frames=[(128, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.JUMP): AnimationCutOut(game, key_atlas="mario-spr", frames=[(76, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.SKID): AnimationCutOut(game, key_atlas="mario-spr", frames=[(700, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.RUN_JUMP): AnimationCutOut(game, key_atlas="mario-spr", frames=[(180, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.RUN): AnimationCutOut(game, key_atlas="mario-spr", frames=[(336, 49, 16, 24), (440, 48, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.SPIN): AnimationCutOut(game, key_atlas="mario-spr", frames=[(232, 112, 16, 24), (284, 112, 16, 24), (336, 112,16, 24), (388, 112, 16, 24)], durations=[0.05, 0.05, 0.05, 0.05]),
            (CharacterPowerup.SMALL, CharacterAction.SWIM): AnimationCutOut(game, key_atlas="mario-spr", frames=[(544, 112, 16, 24), (596, 112, 16, 24), (648, 112, 16, 24)]),
            (CharacterPowerup.SMALL, CharacterAction.DROWN): AnimationCutOut(game, key_atlas="mario-spr", frames=[(544, 112, 16, 24)]),

            # Super

        }


    def set_powerup(self, powerup):
        self.power = powerup

    def set_action(self, action):
        self.action = action


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
        
        
        
        elif self.spin_jump:
            self.action = CharacterAction.SPIN
        
        elif self.vy != 0:
            if self.run_jump:
                self.action = CharacterAction.RUN_JUMP
        
            elif self.vy > 0:
                self.action = CharacterAction.FALL 
            else:
                self.action = CharacterAction.JUMP

        elif self.looking:
            self.action = CharacterAction.LOOK_UP
        
        elif self.skidding:
            self.action = CharacterAction.SKID
        
        elif self.vx != 0:
            if self.p_speed >= 1.0:
                self.action = CharacterAction.RUN
            else:
                self.action = CharacterAction.WALK
        else:
            self.action = CharacterAction.IDLE


    def check_live(self):
        if self.world.time <= 0:
            self.beat = True




    def update(self, delta_time):
        move = 0
     

        # X moving
        if self.keyboard.isPressed(Keys.D):
            move = 1
            self.flip_x = True
        elif self.keyboard.isPressed(Keys.A):
            move = -1
            self.flip_x = False

        self.skidding = (self.on_ground and move != 0 and self.vx != 0 and move != (1 if self.vx > 0 else -1))

        if self.skidding and not self.was_skidding:
            self.world.spawn_effect(SkidDust(self.world, self.x + 16, self.y + self.h - 16))

        self.was_skidding = self.skidding


        # Running
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
        self.looking = (self.keyboard.isPressed(Keys.W) and self.on_ground and abs(self.vx) < 5 and not self.ducking)

        if self.keyboard.isPressed(Keys.S):
            self.ducking = True
            brake = 1400 * delta_time

            if self.vx > 0:
                self.vx = max(0, self.vx - brake)
            elif self.vx < 0:
                self.vx = min(0, self.vx + brake)
    
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


        self.update_action()
        self.check_live()

        super().update(delta_time)


    def move_x(self, dt):
        self.x += self.vx * dt

        for block in self.world.objects:
            if not block.solid:
                continue

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
            if not block.solid:
                continue

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
                    block.hit_from_below(self)


    def render(self, camera):
        animation = self.animations.get((self.power, self.action))

        animation.update()

        x, y = camera.apply(self.x, self.y)

        if self.game.DEBUG:
            self.renderer.renderQuad(position=(x, y), size=(self.w, self.h), g=0, b=0, mode=RenderMode.LINE_LOOP)
        self.renderer.render(animation.getTextureKey(), position=(x, y), size=(48, 72), flx=self.flip_x)


