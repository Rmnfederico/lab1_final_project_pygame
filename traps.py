from obj import *


class Traps(Object):
    pass

class Fire(Object):
    ANIMATION_DELAY = 5

    def __init__(self, x, y , width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire_sprites = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire_sprites["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

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
    pass