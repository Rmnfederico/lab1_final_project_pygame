import threading
import pygame
from config import *
from enemy import Bullet

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3
    JUMP_POWER = 8
    COOLDOWN_FRAMES = 30

    def __init__(self, x, y ,width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

        self.x = x
        self.y = y

        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        #1 Adding a variable to control hit state
        self.hit = False
        #2. Adding a variable to control the 'flashing' effect time when hit
        self.hit_count = 0
        self.dashing = False
        self.dashing_time = 0
        self.dash_cooldown = 0
        self.attached = False
        self.lives = 5
        self.projectiles = pygame.sprite.Group()

    def lose_life(self):
        self.lives -= 1

    def dead(self):
        if self.lives <= 0:
            return True
        else:
            return False

    def jump(self, jump_pwr= None):
        if not jump_pwr:
            self.y_vel = -self.GRAVITY * self.JUMP_POWER
        else:
            self.y_vel = -self.GRAVITY * jump_pwr
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def dash(self):
        if self.dash_cooldown <= 0:
            self.dashing = True
            dash_frames = 20  # Number of frames for the dash
            dash_power = 8  # Velocity increment per frame during the dash

            # Set the direction of the dash based on the player's current direction
            if self.direction == "right":
                dash_direction = 1
            else:
                dash_direction = -1

            # Calculate the target velocity during the dash
            target_x_vel = dash_direction * (self.x_vel + dash_power)

            # Create a separate thread for the dash movement
            threading.Thread(target=self.perform_dash, args=(dash_direction, dash_power, dash_frames, target_x_vel)).start()
            self.dash_cooldown = self.COOLDOWN_FRAMES

    def perform_dash(self, dash_direction, dash_power, dash_frames, target_x_vel):
        # Calculate the velocity increment per frame during the dash
        dash_decrement = abs(self.x_vel) / (dash_frames // 2)

        # Gradually increase the player's velocity towards the target velocity
        for i in range(dash_frames // 2):
            self.x_vel += dash_direction * dash_power
            pygame.time.wait(16)  # Adjust the delay if needed for your desired speed

        # Gradually decrease the player's velocity towards zero
        for i in range(dash_frames // 2):
            self.x_vel -= dash_decrement * dash_direction
            pygame.time.wait(16)  # Adjust the delay if needed for your desired speed

        # Reset the player's velocity to the normal value
        self.x_vel = 0
        self.dashing = False
    
    def throw_projectile(self, rotate_counter):
        if self.direction == "left":
            bomb = Bullet(self.rect.x, self.rect.y, "assets/Items/Throwables/bomb.jpg", -2, True)
        else:
            bomb = Bullet(self.rect.x, self.rect.y, "assets/Items/Throwables/bomb.jpg", 2, True)
        bomb.image = pygame.transform.rotozoom(bomb.image, 0, 0.015)
        #bomb.image = bomb.rotate(rotate_counter)
        bomb.image.set_colorkey((255,255,255))
        self.projectiles.add(bomb)

        #TODO:SHOOT DOWN LOGIC (WHILE IN AIR & PRESSIND DOWN KEY 's')


    #3 Method to control hit state
    def get_hit(self):
        self.hit = True
        self.hit_count = 0
        if not self.dead() and not self.hit:
            self.lose_life()
    
    def check_fall(self):
        if self.rect.bottom >= WIDTH*2:
            self.rect.x = self.x
            self.rect.y = self.y
            #self.hit= True
            #self.lose_life()
            self.get_hit()
            return True
        else: return False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel: int):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):

        self.check_fall()

        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count +=1
        #4 Handling the hit counter for the flashing animation
        if self.hit:
            #if player gets hit, increment the hit counter
            self.hit_count += 1
        #condition to turn off hit state (fps*2 = 2 secs)
        if self.hit_count > fps * 1.5:
            #setting hit state to False when time condition is reached
            self.hit = False
            #resetting hit count as well
            self.hit_count = 0

        if self.dashing:
            self.dashing_time += 1
        if self.dashing_time > fps//2:
            self.dashing = False
            self.dashing_time = 0
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        self.projectiles.update()
        self.update_sprite()


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def attatch_to_wall(self, wall):

        if self.fall_count > 0 and self.rect.bottom <= (wall.rect.bottom-5):
            self.y_vel *= 1/4
            self.jump_count = 0
            self.attached = True

            if self.direction == "right" and self.x_vel == 0:
                self.rect.right = wall.rect.left
            elif self.direction == "left" and self.x_vel == 0:
                self.rect.left = wall.rect.right
            else:
                self.attached = False

        else:
            self.attached = False

    def update_sprite(self):
        sprite_sheet = 'idle'

        if self.dashing:
            sprite_sheet = 'double_jump'
        ################# TODO: CHECK IF IT'S WORKING
        elif self.attached:
            sprite_sheet = 'wall_jump'
            #print(self.SPRITES)
       
        elif self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = 'jump'
            elif self.jump_count > 1:
                sprite_sheet = 'double_jump'
        elif self.y_vel > self.GRAVITY*2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = 'run'

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index] #updates every ANIMATION_DELAY frames
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        self.projectiles.update()

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
