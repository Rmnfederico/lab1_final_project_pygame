import pygame
from config import *
from button import *

class Menu(pygame.sprite.Sprite):
    def __init__(self,x, y, is_active=False):
        super().__init__()
        self.buttons = self.create_buttons()
        self.is_active = is_active
        
        self.image = pygame.Surface((100,100))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x,y))

    # def animate_background(self):
    #     pass

    def animate_button(self):
        pass

    # def loop(self):
    #     pass

    def create_buttons(self):
        print("")

    def draw(self, win):
        if self.is_active:
            pygame.draw.rect(win, (29,23,30),pygame.Rect(0,HEIGHT-83, WIDTH, 83))
            win.blit(self.image, self.rect)

            if self.buttons:
                for button in self.buttons:
                    button.draw(win)

class Widget:
    pass

class MainMenu(Menu):
    def __init__(self, x, y, is_active=False):
        super().__init__(x, y, is_active)
        self.animation_name = "cascade-sprite"
        self.sprites = load_sprite_sheets("","bgs", (int(WIDTH*0.886)), HEIGHT, False)
        
        for i, sprite in enumerate(self.sprites[self.animation_name]):
            self.sprites[self.animation_name][i] = pygame.transform.scale(sprite, (WIDTH, HEIGHT+(HEIGHT*2/3)))

        self.image = self.sprites[self.animation_name][0]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.animation_count = 0
        self.ANIMATION_DELAY = 8

    def create_buttons(self):
        #TODO:
        #buttons list that SHOULD BE external data (JSON)
        #THIS METHOD SHOULD PARSE & INSTANTIATE BUTTONS FROM A JSON FILE 
        buttons_list = []

        flat_btn = pygame.image.load("assets/buttons/layer3.png").convert_alpha()

        btn1 = TextButton(WIDTH/2, 200, flat_btn, 0.3, False, "play", 'assets/fonts/8Bit-44Pl.ttf',"Play",50, offset=[0,-10])
        btn2 = TextButton(WIDTH/2, 340, flat_btn, 0.3, False, "settings", 'assets/fonts/8Bit-44Pl.ttf',"Settings",40, offset=[0,-10])
        btn3 = TextButton(WIDTH/2, 480, flat_btn, 0.3, False, "leaderboard", 'assets/fonts/8Bit-44Pl.ttf',"Leaderboard",30, offset=[0,-10])
        btn4 = TextButton(WIDTH/2, 620, flat_btn, 0.3, False, "quit", 'assets/fonts/8Bit-44Pl.ttf',"Quit",50, offset=[0,-10])

        #btn1 = Button(WIDTH/2, 200, flat_btn, 0.3, False, "play")
        # btn2 = Button(WIDTH/2, 340, flat_btn, 0.3, False, "settings")
        # btn3 = Button(WIDTH/2, 480, flat_btn, 0.3, False, "leaderboard")
        # btn4 = Button(WIDTH/2, 620, flat_btn, 0.3, False, "quit")

        buttons_list.extend([btn1, btn2,btn3, btn4])
        return buttons_list

    def handle_events(self):
        if self.is_active:
            for button in self.buttons:
                if button.name == "play" and button.clicked:
                    self.is_active = False
                if button.name == "quit" and button.clicked:
                    print("PROGRAM FINISHED FROM MENU HANDLER")
                    pygame.quit()
                    exit()

    def update(self):
        if self.is_active:
            for button in self.buttons:
                if button.update():
                    button.image = pygame.transform.rotozoom(pygame.image.load('assets/buttons/layer4.png').convert_alpha(), 0, 0.3)
                    print(f'clicked {button.name} button')
                    self.handle_events()
                else:
                    button.image = pygame.transform.rotozoom(pygame.image.load('assets/buttons/layer3.png').convert_alpha(), 0, 0.3)

            sprites = self.sprites[self.animation_name]
            total_frames = len(sprites)
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % total_frames
            self.image = sprites[sprite_index]
            self.animation_count += 1

            if self.animation_count >= (total_frames*2) * self.ANIMATION_DELAY:
                self.animation_count = 0

    def draw(self, win):
        super().draw(win)

class CharacterSelectMenu(Menu):
    pass

class LevelsMenu(Menu):
    pass

class PauseMenu(Menu):
    pass

class EndLevelMenu(Menu):
    pass