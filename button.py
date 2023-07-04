import pygame
from config import *

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, scale, is_animated, name):
        super().__init__()
        self.image = pygame.transform.rotozoom(image, 0, scale)
        self.rect = self.image.get_rect(center=(x,y))
        self.x = x
        self.y = y
        self.clicked = False
        self.animated = is_animated
        self.name = name

        if self.animated:
            self.sprites = load_sprite_sheets("buttons", name, 40, 13, False)


    def update(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            #TODO: IMPLEMENT ANIMATED BUTTONS (SPRITESHEET)
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
    
    def draw(self, win):
        win.blit(self.image, self.rect)


class TextButton(Button):
    def __init__(self, x, y, image, scale, is_animated, name, font_path, text, size, color=(255,255,255), offset=[0,0]):
        super().__init__(x, y, image, scale, is_animated, name)
        self.font = pygame.font.Font(font_path, size)
        self.text = text
        self.text_render = self.font.render(self.text, True, color)
        self.text_rect = self.text_render.get_rect(center=(x+offset[0],y+offset[1]))

    def update(self):
        return super().update()


    def draw(self, win):
        super().draw(win)
        win.blit(self.text_render, self.text_rect)

