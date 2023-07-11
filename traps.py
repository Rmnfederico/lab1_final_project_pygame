from obj import *


class Trap(Object):
    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height, name)

class Fire(Object):
    ANIMATION_DELAY = 5

    def __init__(self, x, y , width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire_sprites = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire_sprites["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
        self.is_trap = True

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire_sprites[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Saw(Object):
    ANIMATION_DELAY = 5
    X_MAX_VEL, Y_MAX_VEL = 4, 4
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        self.sprites = load_sprite_sheets("Traps", "Saw", width, height)
        self.image = self.sprites["on"][0]
        self.chain_img = self.sprites["chain"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation = 0
        self.animation_name  = "on"
        self.is_trap = True
        self.stopped = False

    def move(self, block_list, clockwise= True):
        #TODO: CHECK LEFT, RIGHT, TOP AND BOTTOM BLOCKS POSITIONS
        if not self.stopped:
            if clockwise:
                self.rect.x += self.X_MAX_VEL

    def stop(self):
        if not self.stopped:
            self.stopped = True

    def loop(self):
        pass


class Spikes(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spikes")
        self.image = pygame.image.load("assets/Traps/Spikes/Idle.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.is_trap = True
