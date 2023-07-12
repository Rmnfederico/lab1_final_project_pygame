import random
import pygame
from config import *
from projectile import Projectile

class Enemy(pygame.sprite.Sprite):
    ANIMATION_DELAY = 5
    GRAVITY = 1
    JUMP_POWER = 8
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
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.lives = None
        self.alive = True
        self.can_move = False
        self.can_shoot = False
        self.can_attack = False
        self.attacking = False
        self.deaggro_counter = 0

    def update_sprite(self):
        #######
        #here goes the logic for class animations

        # Handle Shooting
        # Handle Attack

        #######
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index] #updates every ANIMATION_DELAY frames
        self.animation_count += 1
        self.update()

    def animate_death(self):
        if not self.alive:
            pass #TODO: DEATH SMOKE CLOUD ANIMATION IN SELF.POS
    
    def check_alive(self):
        if self.lives < 1:
            self.alive = False
            self.animate_death()
    
    def get_hit(self):
        self.hit = True
        self.hit_count = 0
        if self.lives > 0:
            self.lives -= 1
        self.check_alive()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
    
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def switch_direction(self):
        if self.direction == "right":
            self.direction = "left"
        else:
            self.direction = "right"

    def handle_vertical_collision(self, objects):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed()
                #TODO: COMMENTED TO IMPLEMENT JUMP & CHASE()
                # elif self.y_vel < 0: 
                #     self.rect.top = obj.rect.bottom
                #     self.hit_head()
                collided_objects.append(obj)

        return collided_objects

    def check_horizontal_collision(self, objects, dx):
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if self.rect.bottom > (obj.rect.top+15):
                    if self.x_vel > 0:
                        self.rect.x -= 5
                        self.switch_direction()
                    else:
                        self.rect.x += 5
                        self.switch_direction()
                    self.x_vel *= -1


    def handle_move(self, objects):
        collide_left = self.check_horizontal_collision(objects, -self.x_vel*2)
        collide_right = self.check_horizontal_collision(objects, self.x_vel*2)

        if collide_left or collide_right:
            self.x_vel *= -1
        #TODO: NECESSARY? CHECK IF IMPLEMENTATION NEEDED
        vertical_collide = self.handle_vertical_collision(objects)

    # def attack(self, player):
    #     if self.can_attack:
    #         print("Attacking")
    #         attack_distance = 20
    #         if player.rect.top < self.rect.bottom or player.rect.bottom > self.rect.top:
    #             if (self.rect.centerx - player.rect.centerx) < 10 or player.rect.centerx - self.rect.centerx < 10:
    #                 print(f'enemy x:{self.rect.centerx} | player x:{player.rect.centerx}')
    #                 return True
    #     else: return False

    def jump(self, jump_pwr= None):
        if not jump_pwr:
            self.y_vel = -self.GRAVITY * self.JUMP_POWER
        else:
            self.y_vel = -self.GRAVITY * jump_pwr
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def attack(self, player):
        if self.can_attack:
            attack_distance = 70
            if player.rect.top < self.rect.bottom and player.rect.bottom > self.rect.top:
                if abs(self.rect.centerx - player.rect.centerx) < attack_distance:
                    print("Attacking")
                    self.x_vel = 0
                    self.attacking = True
            else:
                self.attacking = False
            if self.x_vel < 1:
                #self.patrol()
                self.chase(player)
                #TODO: FIX IS HERE, MODIFYING rect.x velocity
                #TODO: CHASE METHOD MAY WORK HERE
                #self.rect.x += 4
            #print(f'aggro count:{self.deaggro_counter}')
            # self.deaggro_counter +=1
            # if self.deaggro_counter >= 90:
            #     self.attacking = False
            #     self.deaggro_counter = 0
            #     self.patrol()
            #     else:
            #         self.deaggro_counter += 1
            # if self.deaggro_counter >= 120:
            #     self.attacking = False

    def chase(self, player):
        if self.lives == 1 and self.can_move:
            if self.rect.centerx > player.rect.centerx:
                self.rect.x -= self.x_vel
            else:
                self.rect.x += self.x_vel

            if (player.rect.y+120) < self.rect.y:
                #TODO: REFACTOR JUMP W/ TIMER AND DISTANCE CALC. BEOFRE JUMPING
                self.jump()
                

    def patrol(self):
        if self.can_move:
            if self.rect.x <= self.x:  # Change the condition here
                self.direction = self.right
                self.x_vel = self.X_MAX_VEL  # Change the sign here
            elif self.rect.x >= (self.x + 550):  # Change the condition here
                self.direction = self.left
                self.x_vel = -self.X_MAX_VEL  # Change the sign here
            self.rect.x += self.x_vel

    def loop(self, player=None):
        #Here handle:
        
        # - Patrol
        #if not self.attacking:
        self.patrol()

        # - Attack
        self.attack(player)
        # - Jump
        # - Move
        # - Gravity Apply / Fall velocity
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)
        self.fall_count +=1
        self.rect.y += self.y_vel
        # - Hit counter
        if self.hit:
            self.hit_count += 1
        if self.hit_count > FPS * 1.5:
            self.hit = False
            self.hit_count = 0
        # - Collisions
        # - Etc.
        self.update_sprite()

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Bunny(Enemy):
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
        self.can_move = True
    
    def loop(self):
        super().loop()

    #def update(self):

    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True
        if self.hit:
            self.sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                self.sprite_sheet = 'jump'
            # elif self.jump_count > 1:
            #     sprite_sheet = 'double_jump'
        elif self.y_vel > self.GRAVITY*2:
            self.sprite_sheet = "fall"
        elif self.x_vel != 0:
            self.sprite_sheet = 'run'
        super().update_sprite()

class Plant(Enemy):
    left, right = "right", "left"

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "plant")
        self.SPRITES = load_sprite_sheets("Enemies", "Plant", 44, 42, True)
        self.direction = self.left
        self.image = self.SPRITES["idle_"+ self.direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.default_sprite = "attack"
        self.can_shoot = True
        self.shot_timer = 0
        self.active_bullets = pygame.sprite.Group()
        self.lives = 2

    def loop(self):
        #self.shoot()
        super().loop()

    def track_player(self,player):
        if self.rect.left < player.rect.right:
            self.direction = self.right
        elif self.rect.right > player.rect.left:
            self.direction = self.left

    def shoot(self, offset_x, player):
        self.shot_timer += 1
        if self.shot_timer >= 90:
            self.shot_timer = 0
            self.track_player(player)
            if self.direction == self.left:
                bullet = Projectile(self.rect.x - offset_x, (self.rect.y+15), "assets/Enemies/Plant/Bullet.png", -5)
            else:
                bullet = Projectile(self.rect.x - offset_x, (self.rect.y+15), "assets/Enemies/Plant/Bullet.png", 5)
            self.active_bullets.add(bullet)

    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True
        
        if self.hit:
            self.sprite_sheet = "hit"
        elif not self.hit:
            self.sprite_sheet = self.default_sprite
        super().update_sprite()

    def update(self):
        self.active_bullets.update()
        super().update()
        
    def draw(self, win, offset_x, offset_y):
        #self.active_bullets.draw(win)
        super().draw(win, offset_x, offset_y)

class Chameleon(Enemy):
    X_MAX_VEL, Y_MAX_VEL = 4, 4
    left, right = "right", "left"

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "chameleon")
        self.SPRITES = load_sprite_sheets("Enemies", "Chameleon", 84, 38, True)
        self.direction = self.left
        self.image = self.SPRITES["idle_"+ self.direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.default_sprite = "idle"
        self.lives = 3
        self.can_move = True
        self.can_attack = True

    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True

        elif self.hit:
            self.sprite_sheet = "hit"
        elif self.attacking:
            self.sprite_sheet = "attack"
        elif self.x_vel != 0:
            self.sprite_sheet = 'run'
        elif self.x_vel == 0:
            self.sprite_sheet = 'idle'
        super().update_sprite()

class Ghost(Enemy):
    left, right = "right", "left"
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "ghost")
        self.SPRITES = load_sprite_sheets("Enemies", "Ghost", 44, 30, True)
        self.direction = self.left
        self.image = self.SPRITES["idle_"+ self.direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.default_sprite = "idle"
        self.lives = 3
        self.can_move = False
        self.can_attack = False
        self.desappear = False
    
    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True

        elif self.hit:
            self.sprite_sheet = "hit"
        elif self.desappear:
            self.sprite_sheet = "desappear"
        # elif self.x_vel != 0:
        #     self.sprite_sheet = 'run'
        elif self.x_vel == 0:
            self.sprite_sheet = 'idle'
        return super().update_sprite()

class Slime(Enemy):
    left, right = "right", "left"
    X_MAX_VEL, Y_MAX_VEL = 4, 4

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "slime")
        self.SPRITES = load_sprite_sheets("Enemies", "Slime", 44, 30, True)
        self.direction = self.left
        self.image = self.SPRITES["idle-run_"+ self.direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.default_sprite = "idle-run"
        self.lives = 3
        self.can_move = True
        self.can_attack = False

    def update_sprite(self):
        if not self.ignore_default_sprite:
            self.sprite_sheet = self.default_sprite
            self.ignore_default_sprite = True

        elif self.hit:
            self.sprite_sheet = "hit"
        elif self.x_vel != 0:
            self.sprite_sheet = 'idle-run'
        elif self.x_vel == 0:
            self.sprite_sheet = 'idle-run'
        return super().update_sprite()
    
class PumpkingBoss(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "pumpking_boss")

    def update_sprite(self):
        return super().update_sprite()
