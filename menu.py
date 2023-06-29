import pygame

class Menu:
    def __init__(self,x, y, name, is_active=False):
        self.name = name
        self.is_active = is_active
        self.image = None
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x,y))
        self.buttons = None
    
    def click_button(self, mouse_pos):
        pass

    def animate_button(self):
        pass

    def update(self):
        pass
    
    def loop(self):
        pass
    
    def draw(self, win):
        win.blit(self.image, self.rect)

class MainMenu(Menu):
    pass

class PauseMenu(Menu):
    pass

class EndLevelMenu(Menu):
    pass

### ????
class Button:
    pass

class Widget:
    pass