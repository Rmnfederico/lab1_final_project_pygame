import pygame
from config import *

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        self.is_trap = False

    #MOST LIKELY NOT NECESSARY HERE; JUST IN ITEMS/TRAPS/PLATFORMS(NOT ALL OF THEM)
    def update(self): 
        pass

    def loop(self):
        pass

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y , size):
        super().__init__(x, y, size, size)
        block = load_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)



