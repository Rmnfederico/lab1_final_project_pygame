import random
import pygame
from config import *

class Enemy(pygame.sprite.Sprite):
    ANIMATION_DELAY = 5 
    #SPRITES = load_sprite_sheets() -> TO CHILD CLASSES?
    
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.name = name
        #needed?
        self.width = width
        self.height = height

        #needed x2?
        self.x = x
        self.y = y

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = None

        self.sprite_sheet = None

        self.default_sprite = None
        self.ignore_default_sprite = False
        self.direction = "left"
        self.animation_count = 0
        self.hit = False
        self.hit_count = 0
        self.lives = None

    def update_sprite(self):
        #######
        #here goes the logic for class animations
        #######
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index] #updates every ANIMATION_DELAY frames
        self.animation_count += 1
        self.update()

    def get_hit(self):
        self.hit = True
        self.hit_count = 0
        if self.lives:
            self.lives -= 1
    
    def loop(self):
        #Here handle:
        # - Attack
        # - Jump
        # - Move
        # - Fall velocity
        # - Hit counter
        # - Hit state
        # - Hit counter
        # - Etc.
        self.update_sprite()

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Bunny(Enemy):
    GRAVITY = 1
    left, right = "right", "left"
    X_MAX_VEL, Y_MAX_VEL = 4, 4

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "bunny")
        self.SPRITES = load_sprite_sheets("Enemies", "Bunny", 34, 44, True)
        self.direction = self.left
        self.image = self.SPRITES["idle_"+ self.direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.default_sprite = "idle"
        self.lives = 3
    
    def loop(self):
        self.patrol(True)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > FPS * 1.5:
            self.hit = False
            self.hit_count = 0

        super().loop()

    #def jump()

    def patrol(self, on=True):
        if on:
            if self.rect.x <= self.x:  # Change the condition here
                self.direction = self.right
                self.x_vel = self.X_MAX_VEL  # Change the sign here
            elif self.rect.x >= (self.x + 160):  # Change the condition here
                self.direction = self.left
                self.x_vel = -self.X_MAX_VEL  # Change the sign here

            self.rect.x += self.x_vel

    #def update(self):

    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True
        #5 Implementing hit animation (IMPORTANT TO PUT IT AT THE TOP)
        if self.hit:
            self.sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = 'jump'
            # elif self.jump_count > 1:
            #     sprite_sheet = 'double_jump'
        elif self.y_vel > self.GRAVITY*2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            self.sprite_sheet = 'run'
        super().update_sprite()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path, BULLET_SPEED):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load(img_path).convert_alpha())
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = BULLET_SPEED

    def to_pieces(self):
        self.image = pygame.transform.scale2x(pygame.image.load(r"assets\Enemies\Plant\Bullet Pieces.png").convert_alpha())

    def update(self):
        self.rect.x += self.speed

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class Plant(Enemy):
    left, right = "right", "left"

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "plant")
        self.SPRITES = load_sprite_sheets("Enemies", "Plant", 44, 42, True)
        self.direction = self.left
        self.image = self.SPRITES["idle_"+ self.direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.default_sprite = "attack"
        self.shot_timer = 0
        self.active_bullets = pygame.sprite.Group()
        self.lives = 2

    def loop(self):
        #self.shoot()
        if self.hit:
            self.hit_count += 1
        if self.hit_count > FPS * 1.5:
            self.hit = False
            self.hit_count = 0
        super().loop()

    def shoot(self, offset_x):
        self.shot_timer += 1
        if self.shot_timer >= 90:
            self.shot_timer = 0
            if self.direction == self.left:
                bullet = Bullet(self.rect.x- offset_x, (self.rect.y+15), "assets/Enemies/Plant/Bullet.png", -5)
            else:
                bullet = Bullet(self.rect.x - offset_x, (self.rect.y+15), "assets/Enemies/Plant/Bullet.png", 5)
            self.active_bullets.add(bullet)

    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True
        
        if self.hit:
            self.sprite_sheet = "hit"
        super().update_sprite()

    def update(self):
        self.active_bullets.update()
        super().update()
        
    def draw(self, win, offset_x, offset_y):
        #self.active_bullets.draw(win)
        super().draw(win, offset_x, offset_y)