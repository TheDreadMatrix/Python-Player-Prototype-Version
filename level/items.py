from level.entities import Item




class Mushroom(Item):
    def __init__(self, world, x=0, y=0):
        super().__init__(world=world, x=x, y=y, w=48, h=48)

        self.assets.regCutOutImage("mushroom", "tiles", x=291, y=30, w=16, h=16)

        self.speed = 100
        self.dir = 1

    def update(self, delta_time):
        self.vx = self.dir * self.speed

        super().update(delta_time)

        if self.intersects(self.world.main_entity):
            self.on_collect(self.world.main_entity)


    def on_spawn_from_block(self, block):
        self.x = block.x
        self.y = block.y - self.h
        self.vy = -500


    def on_collect(self, player):
        player.set_action(5)
        self.dead = True


    def move_x(self, delta_time):
        self.x += self.vx * delta_time
        
        for block in self.world.objects:
            if not block.solid:
                continue
        
            if self.intersects(block):        
                if self.vx > 0:
                    self.dir *= -1
                    self.x = block.x - self.w
        
                elif self.vx < 0:
                    self.dir *= -1
                    self.x = block.x + block.w


    def move_y(self, delta_time):
        self.vy += self.gravity * delta_time
        self.y += self.vy * delta_time
        
        self.on_ground = False
                
        
        for block in self.world.objects:
            if not block.solid:
                continue
        
            if self.intersects(block):        
                if self.vy > 0:
                    self.y = block.y - self.h
                    self.vy = 0
                    self.on_ground = True
                            
                elif self.vy < 0:
                    self.y = block.y + block.h
                    self.vy = 0


    def render(self, camera):
        x, y = camera.apply(self.x, self.y)

        self.renderer.render("mushroom", position=(x, y), size=(self.w, self.h))
    


