from level.entities import Block, Type, Item


class HitBlock(Block):
    def __init__(self, world):
        super().__init__(world)

        self.bump_offset = 0
        self.bump_velocity = 0

    def update(self, dt):
        if self.bump_velocity != 0 or self.bump_offset != 0:
            self.bump_offset += self.bump_velocity * dt
            self.bump_velocity += 900 * dt
    
            if self.bump_offset > 0:
                self.bump_offset = 0
                self.bump_velocity = 0


    def hit_from_below(self, entity):
        if self.bump_velocity != 0 or self.bump_offset != 0:
            return
        
        self.bump_velocity = -100

    def render(self, camera):
        x, y = camera.apply(0, 0) 
            
        if self.animation is not None:
            self.animation.update()
            texture = self.animation.getTextureKey()
        else:
            texture = self.texture
            
        self.renderer.render(texture, position=(self.x + x, self.y + y + self.bump_offset), size=(self.w, self.h))
        


class LootBlock(HitBlock):
    def __init__(self, world, loot: Type[Item]):
        super().__init__(world)

        self.used = False
        
        self.loot = loot

    
    def hit_from_below(self, entity):
        super().hit_from_below(entity)

        if self.used:
            return

        #self.used = True

    
        item = self.world.spawn(self.loot(self.world, x=self.x, y=self.y - 48))
        item.on_spawn_from_block(self)    

        #self.texture = "used-block"
        #self.animation = None


    

class MessageBlock(HitBlock):
    def __init__(self, world, text):
        super().__init__(world)

        self.text = text

    def hit_from_below(self, entity):
        super().hit_from_below(entity)
        self.world.show_message(self.text)