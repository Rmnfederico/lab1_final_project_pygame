import pygame

class Menu:
    def __init__(self,x, y, name, is_active=False):
        self.name = name
        self.is_active = is_active
        self.image = None
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x,y))
        self.buttons = []
    
    def click_button(self, mouse_pos):
        pass

    def animate_background(self):
        pass

    def animate_button(self):
        pass

    def update(self):
        pass
    
    def loop(self):
        pass
    
    def draw(self, win):
        win.blit(self.image, self.rect)

class Button:
    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.rotozoom(image, 0, scale)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, win):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        win.blit(self.image, self.rect)

        return action

class ButtonText(pygame.sprite.Sprite): #inherits sprite to use group.draw()
    def __init__(self,image,x,y,text):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.font = pygame.font.SysFont("Arial Narrow", 40)
        self.text = text
        self.text_render = self.font.render(self.text,True,"black")
        self.text_rect = self.text_render.get_rect(center=self.rect.center)
        self.select = False

    def update(self,screen):
        if self.select: #select = colisionando con el mouse
            self.image = pygame.transform.scale(pygame.image.load(r"sprite juego\image_button_select.png"),(200,60)).convert_alpha()
        else:
            self.image = pygame.transform.scale(pygame.image.load(r"sprite juego\image_button.png"),(200,60)).convert_alpha()


class Widget:
    pass

class MainMenu(Menu):
    pass

class LevelsMenu(Menu):
    pass

class PauseMenu(Menu):
    pass

class EndLevelMenu(Menu):
    pass