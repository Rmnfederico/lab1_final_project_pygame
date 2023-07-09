from obj import *

class Item(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width,height,name)
        self.sprites = load_sprite_sheets("Items", "Fruits", width, height)
        self.consumables_sprites = load_sprite_sheets("Items", "Consumables", width, height)
        self.sprites.update(self.consumables_sprites)

        self.resize_imgs("bomb_2",0.7)
        self.resize_imgs("coin",0.5)
        self.resize_imgs("heart",0.6)


        self.image = self.sprites[name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = name
        self.grabbed = False
        self.dissapear_timer = 0

    def resize_imgs(self, sprite_name, scale):
        for i, img in enumerate(self.sprites[sprite_name]):
            self.sprites[sprite_name][i] = pygame.transform.rotozoom(img, 0, scale)

    def update_sprite(self):
        if self.grabbed:
            self.animation_name = "collected"
            self.dissapear_timer += 1
        if self.dissapear_timer >= 30:
            self.dissapear_timer = 30
        #self.update()


    def update(self):
        self.update_sprite()
        sprites = self.sprites[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def draw(self, win, offset_x, offset_y):
        if self.dissapear_timer < 30:
            super().draw(win, offset_x, offset_y)


class Coin(Object):
    pass

class Life(Object):
    pass