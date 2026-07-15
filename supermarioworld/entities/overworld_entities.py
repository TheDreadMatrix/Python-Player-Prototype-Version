from supermarioworld.typing.gametype import GameType
from supermarioworld.typing.audio_type import BasicSound
from supermarioworld.johnson import Johnson

from supermarioworld.rendering.animation import AnimationCutOut

import pygame as pg
import math





class OverWorldPlayer:
    def __init__(self, game: GameType, map_ref: str, move_speed: int=160):
        self.game = game

        self.DEFAULT_NODE = {"title": "node-cant-be-found"}
        self.MAP_REF = map_ref

        # Speed
        self.move_speed = move_speed


        # Nodes
        game.player.current_overworld = map_ref
        

        self.main_nodes = Johnson(game.paths.ConfigPath(f"overworld/nodes/{map_ref}.json")).readData()

        self.current_node = self.main_nodes.get(game.player.current_overworld_level, self.DEFAULT_NODE)

        self.current_node_key = game.player.current_overworld_level


        
        self.position = self.current_node.get("position", (0, 0))
        self.moving = False

        self.redirecting = False
        self.redirect_timer = 0
        self.redirect_scene = ""

        self.path = []
        self.path_animations = []

        self.path_index = 0
        self.target = None
        

        
        # Rendering
        self.renderer = game.renderer
        self.request = game.request
        

        game.assets.regAtlas("chr-spr", "overworld/overworld-sprites.png")


        self.animation_choose = AnimationCutOut(game, "chr-spr", frames=[(8, 136, 16, 16)], durations=[], key_images=["mc-1"])

        self.animation_left = AnimationCutOut(game, "chr-spr", frames=[(8, 64, 16, 16), (32, 64, 16, 16)], durations=[0.2, 0.2], key_images=["ml-1", "ml-2"])
        self.animation_down = AnimationCutOut(game, "chr-spr", frames=[(8, 16, 16, 16), (32, 16, 16, 16), (56, 16, 16, 16), (80, 16, 16, 16)], durations=[0.3, 0.5, 0.3, 0.5], key_images=["md-1", "md-2", "md-3", "md-4"])
        self.animation_up = AnimationCutOut(game, "chr-spr", frames=[(8, 40, 16, 16), (32, 40, 16, 16), (56, 40, 16, 16), (80, 40, 16, 16)], durations=[0.2, 0.4, 0.2, 0.4], key_images=["mu-1", "mu-2", "mu-3", "mu-4"])
        self.animation_right = AnimationCutOut(game, "chr-spr", frames=[(56, 64, 16, 16), (80, 64, 16, 16)], durations=[0.2, 0.2], key_images=["mr-1", "mr-2"])

        self.current_animation = self.animation_down

        self.animation_dict = {
            "left": self.animation_left,
            "down": self.animation_down,
            "up": self.animation_up,
            "right": self.animation_right
        }

        

    def _getTitleNode(self):
        return self.current_node.get("title", "unnamed-title-node")
    
    def startMove(self, node_data):
        if self.moving:
            return
        
        if not self.game.player.hasOverworldNodeOpened(node_data.get("target")):
            return 

        self.moving = True
        self.path = node_data.get("path", [])
        self.path_animations = node_data.get("path-animation", [])
        self.path_index = 0
        self.target = node_data.get("target")

    def getCurrentPathAnimation(self):
        if self.path_index >= len(self.path_animations):
            return self.animation_down

        animation_name = self.path_animations[self.path_index]

        return self.animation_dict.get(animation_name, self.animation_down)


    def updatePlayer(self, sound_if_passed: BasicSound):
        # Animations
        self.current_animation = self.getCurrentPathAnimation()
        self.current_animation.update()
        self.animation_down.update()

        

        if self.redirecting:
            self.redirect_timer += self.game.delta_time
            if self.redirect_timer > 2.5:
                self.game.player.current_overworld = self.MAP_REF
                self.game.player.current_overworld_level = self.current_node_key
                
                self.game.player.save()
                self.request.redirectScene(self.redirect_scene)

            return

        if not self.moving:
            return

        if self.path_index >= len(self.path):
            self.current_node_key = self.target
            self.current_node = self.main_nodes.get(self.target, self.DEFAULT_NODE)
            self.position = self.current_node.get("position", (0, 0))

            # Play sound when we passed the node
            sound_if_passed.play()

            self.moving = False
            self.target = None
            self.current_animation = self.animation_down
            return

        target_x, target_y = self.path[self.path_index]

        dx = target_x - self.position[0]
        dy = target_y - self.position[1]

        distance = math.hypot(dx, dy)

        step = self.move_speed * self.game.delta_time

        if distance <= step:
            self.position = (target_x, target_y)
            self.path_index += 1
            return

        vx = dx / distance
        vy = dy / distance

        self.position = (self.position[0] + vx * step, self.position[1] + vy * step)
        
        



    def handleEventNodes(self, event):
        if event.type == pg.QUIT:
            self.game.player.current_overworld = self.MAP_REF
            self.game.player.current_overworld_level = self.current_node_key
            
            self.game.player.save()

        if self.moving:
            return
        
        if self.redirecting:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                up_node = self.current_node.get("up")
                if up_node:
                    self.startMove(up_node)
                

            if event.key == pg.K_s:
                down_node = self.current_node.get("down")
                if down_node:
                    self.startMove(down_node)
                

            if event.key == pg.K_d:
                right_node = self.current_node.get("right")
                if right_node:
                    self.startMove(right_node)
                

            if event.key == pg.K_a:
                left_node = self.current_node.get("left")
                if left_node:
                    self.startMove(left_node)
                

            # Rederecting to scene
            if event.key == pg.K_q:
                redirect = self.current_node.get("redirect")
                if redirect and not self.moving:
                    self.redirecting = True
                    self.redirect_scene = redirect


            # Exit to menu
            if event.key == pg.K_e:
                if not self.moving:
                    self.redirecting = True 
                    self.redirect_scene = "base:menu"
                    
                    



    def renderPlayer(self, camera, r=1, g=1, b=1): 
        x, y, = camera.apply(self.position[0], self.position[1])

        if self.redirecting and self.redirect_scene != "base:menu":
            animation = self.animation_choose

        elif self.moving:
            animation = self.current_animation

        else:
            animation = self.animation_down

        self.renderer.render(animation.getTextureKey(), size=(48, 48), position=(x, y), r=r, g=g, b=b)
        
        
