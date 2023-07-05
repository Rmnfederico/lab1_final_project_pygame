import pygame
from config import *

class Projectile(pygame.sprite.Sprite):
    GRAVITY = 1
    VOLLEY_POWER = 1

    def __init__(self, x, y, img_path, BULLET_SPEED, volley=False):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load(img_path).convert_alpha())
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = BULLET_SPEED
        self.volley = volley
        self.y_vel = 0
        self.fall_count = 0
        self.upwards = False
        #self.explosion_sprite = load_sprite_sheets() #TODO:

    def to_pieces(self):
        self.image = pygame.transform.scale2x(pygame.image.load(r"assets\Enemies\Plant\Bullet Pieces.png").convert_alpha())

    def rotate(self, angle):
        return pygame.transform.rotozoom(self.image, angle, 1)

    def apply_volley(self, FPS):
        if not self.upwards:
            self.y_vel = -1
            self.upwards = True
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)


    def update(self):
        if self.volley:
            self.apply_volley(FPS)
            self.rect.y += self.y_vel
            self.fall_count += 0.01

        self.rect.x += self.speed

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))