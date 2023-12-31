import copy
import random
import pygame
from config import *
from enemy import Enemy
from items import Item

from obj import Block

class Level:
    def __init__(self, name, bg_name, bg_sprite, level_number, terrain, player, enemies, enemies_group, traps, platforms, coins, fruits, lifes, timer, menus, next_level, unlocked): #replace items w/ a JSON
        
        self.original_terrain = terrain
        self.original_player = player
        self.original_enemies = enemies
        self.original_traps = traps
        self.original_platforms = platforms
        self.original_coins = coins
        self.original_fruits = fruits
        self.original_lifes = lifes
        
        self.name = name
        self.bg_animation_name = bg_name
        self.bg_sprite = bg_sprite
        print(f'bg_sprite:{bg_sprite} | anim. name:{self.bg_animation_name}')
        self.bg_image = bg_sprite[self.bg_animation_name][0]
        self.bg_animation_delay = 10
        self.bg_animation_count = 0

        self.terrain = terrain
        self.player = player
        self.enemies = enemies

        #self.enemies_group = enemies_group
        self.enemies_group = pygame.sprite.Group()
        self.enemies_group.add(*enemies)

        self.platforms = platforms
        self.traps = traps
        self.objects = [*terrain, *enemies, *traps]

        self.objects_group = pygame.sprite.Group()
        self.objects_group.add(*terrain, *traps)

        self.items = pygame.sprite.Group(*(self.spawn_random_items(coins, fruits, lifes)))
        self.pause_menu = menus["pause_menu"]
        self.endlevel_menu = menus["endlevel"]
        self.game_over_menu = menus["game_over"]
        self.menus = [self.pause_menu, self.endlevel_menu, self.game_over_menu]
        self.paused = False
        self.finished = False
        self.game_over = False
        self.is_active = False
        self.timer = timer * FPS
        self.level_number = level_number
        self.next_level = next_level
        self.unlocked = unlocked

        self.offset_x = 0
        self.offsext_y = 0
        self.scroll_area_width = 150

    def check_state(self):
        if self.timer <= 0 or self.player.lives == 0:
            self.game_over = True
            self.is_active = False
            self.game_over_menu.is_active = True
        elif len(self.enemies_group) == 0:
            self.finished = True

    def calculate_offset(self):
        if ((self.player.rect.right - offset_x >= WIDTH - self.scroll_area_width) and self.player.x_vel > 0) or (
            (self.player.rect.left - offset_x <= self.scroll_area_width) and self.player.x_vel < 0):
            offset_x += self.player.x_vel
        if ((self.player.rect.bottom - offset_y >= HEIGHT - self.scroll_area_width) and self.player.y_vel > 0) or (
            (self.player.rect.top - offset_y <= self.scroll_area_width) and self.player.y_vel < 0):
            offset_y += self.player.y_vel

    def unlock_next(self):
        if self.finished:
            self.next_level.unlocked = True

    def search_furthest_block(self, left=True):
        furthest = None
        for block in self.terrain:
            if left:
                if furthest is None or block.rect.x < furthest:
                    furthest = block
            else:
                if furthest is None or block.rect.x > furthest:
                    furthest = block
        return furthest

    def spawn_random_items(self, coins, fruits, lifes):
        random_items = []
        coins_counter = 0
        fruits_counter = 0
        lifes_counter = 0
        total_items = coins + fruits + lifes
        blocks = [block for block in self.terrain if isinstance(block, Block)]
        for i in range(total_items):
            block = random.choice(blocks)
            #item = random.choice(["coin", "one_up", "apple", "cherries", "bananas"])
            if coins_counter < coins:
                random_items.append(Item(block.rect.x, block.rect.y-64, 32, 32, "coin"))
                coins_counter += 1
            elif fruits_counter < fruits:
                fruit_name = random.choice(["apple", "bananas", "cherries"])
                random_items.append(Item(block.rect.x, block.rect.y-64, 32, 32, fruit_name))
                fruits_counter += 1
            elif lifes_counter < lifes:
                random_items.append(Item(block.rect.x, block.rect.y-64, 32, 32, "1up"))
                lifes_counter += 1
        return random_items

    def calculate_score(self):
        total_score = 0
        total_score += (self.player.coins*10)
        total_score += (self.player.fruits*5)
        total_score += (self.timer*20)
        return total_score

    def draw_player_lives(self, window):
        pass

    def draw_grabbed_items(self, window):
        pass

    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_menu.is_active = True

    def show_endlevel_menu(self):
        if self.finished:
            final_score = self.calculate_score()
            self.endlevel_menu.is_active = True

    def init_entities(self, player, enemies, traps, platforms):
        pass

    # def save_initial_entities(self):
    #     self.original_terrain = terrain
    #     self.original_player = player
    #     self.original_enemies = enemies
    #     self.original_traps = traps
    #     self.original_platforms = platforms
    #     self.original_coins = coins
    #     self.original_fruits = fruits

    def reset_entities(self):
        self.terrain = self.original_terrain
        self.player = self.original_player
        self.enemies = self.original_enemies
        self.traps = self.original_traps
        self.platforms = self.original_platforms
        self.items = pygame.sprite.Group(*self.spawn_random_items(self.original_coins, self.original_fruits, self.original_lifes))

    def restart_level(self):
        for button in self.pause_menu.buttons:
            if button.name == "restart" and button.clicked:
                self.reset_entities()
                self.offset_x, self.offset_y = self.player.x, self.player.y


    def animate_background(self):
        sprites = self.bg_sprite[self.bg_animation_name]
        total_frames = len(sprites)
        sprite_index = (self.bg_animation_count // self.bg_animation_delay) % total_frames
        self.bg_image = sprites[sprite_index]
        self.bg_animation_count += 1

        if self.bg_animation_count >= (total_frames*2) * self.bg_animation_delay:
            self.bg_animation_count = 0

    def handle_events(self):
        pass

    def update(self):
        if self.is_active and not self.paused and not self.finished:
            self.check_state()
            
            self.player.loop(FPS)

            if self.player.check_fall():
                self.offset_x, self.offset_y = self.player.x, self.player.y
            
            self.traps.loop()
            self.items.update() #TODO: THIS IS A GROUP.

            for enemy in self.enemies:
                if not enemy.can_attack:
                    enemy.loop()
                else:
                    enemy.loop(self.player)
                enemy.handle_move(self.terrain)
                if enemy.name == "plant" and enemy.alive:
                    enemy.shoot(self.offset_x, self.player)
                    if enemy.active_bullets:
                        if pygame.sprite.spritecollide(self.player, enemy.active_bullets, True):
                            self.player.get_hit()
            
            self.calculate_offset()


    def create_platform(self, height_multiplier, start, end):
        return [Block(i* block_size, HEIGHT - block_size*height_multiplier, block_size) for i in range(start // block_size, end // block_size)]

    def create_wall(self, height, start, end):
        return [Block(block_size, i* (HEIGHT - block_size*height), block_size) for i in range(start // block_size, end // block_size)]


    def control_traps(self):
        pass

    def trigger_traps(self):
        pass

    def disable_traps(self):
        pass
    
    def is_finished(self):
        if not self.finished:
            self.finished = True

    def handle_vertical_collision(self):
        collided_objects = []
        for obj in self.objects:
            if pygame.sprite.collide_mask(self.player, obj):
                if self.player.y_vel > 0:
                    self.player.rect.bottom = obj.rect.top
                    self.player.landed()
                elif self.player.y_vel < 0:
                    self.player.rect.top = obj.rect.bottom
                    self.player.hit_head()
                #
                collided_objects.append(obj)
        return collided_objects

    def collide(self, dx):
        self.player.move(dx, 0)
        self.player.update()
        collided_object = None
        for obj in self.objects:
            if pygame.sprite.collide_mask(self.player, obj):
                collided_object = obj
                break
        self.player.move(-dx, 0)
        self.player.update()
        return collided_object

    def handle_player_move(self):
        keys = pygame.key.get_pressed()

        self.player.x_vel = 0 #This way no flag is needed to know if player is moving
        
        collide_left = self.collide(-PLAYER_VEL *2)
        collide_right = self.collide(PLAYER_VEL *2)

        if keys[pygame.K_a] and not collide_left:
            self.player.move_left(PLAYER_VEL)
        if keys[pygame.K_d] and not collide_right:
            self.player.move_right(PLAYER_VEL)

        vertical_collide = self.handle_vertical_collision()

        to_check = [collide_left, collide_right, *vertical_collide]

        for obj in to_check: #get_trap_names() List to replace "fire"
            
            if obj and isinstance(obj, Block):
                self.player.attatch_to_wall(obj)

            if obj and obj.name == "fire" and obj.animation_name == "on" and not self.player.hit:
                self.player.get_hit()
                print("COLLIDING WITH FIRE")

            if obj and isinstance(obj, Enemy) and self.player.rect.bottom <= obj.rect.top:
                obj.get_hit()
                self.player.jump(self.player.JUMP_POWER/2)
                print("HIT ENEMY ON TOP")
                print(f'lives:{obj.lives}')
                if not obj.alive:
                    self.objects.remove(obj) #TODO:ANIMATE DEATH AS WELL!!!
                    obj.kill() #

                break

            elif obj and isinstance(obj, Enemy) and not self.player.hit and not obj.hit:
                self.player.get_hit()

    def handle_bombs_collision(self):
        for bomb in self.player.projectiles:

            for obj in self.objects_group:
                if pygame.sprite.collide_mask(bomb, obj):
                    print(f'collided w/ {obj}')
                    self.player.projectiles.remove(bomb)
                    break

            for enemy in self.enemies_group:
                if pygame.sprite.collide_mask(bomb, enemy):
                    print(f'collided with {type(enemy)}')
                    
                    #TODO:REFACTOR THIS LOGIC TO SOME FUNC/METHOD
                    enemy.get_hit() 
                    self.player.projectiles.remove(bomb)
                    if not enemy.alive:
                        self.enemies_group.remove(enemy)
                        self.objects.remove(enemy) #TODO:ANIMATE DEATH AS WELL!!!
                        enemy.kill() #

    def handle_items_collision(self):
        items_collision = pygame.sprite.spritecollide(self.player, self.items_group, False)
        for item in items_collision:
            if not item.grabbed:
                item.grabbed = True
                self.player.grab_item(item)
                print(f"COLLISION w/ {item.name}")

    def draw_all(self, window):
        if any(menu.is_active for menu in self.menus):
            for menu in self.menus:
                if menu.is_active:
                    menu.draw(window)
                    break
        else:
            #TODO: HERE DRAW BACKGROUND
            # for tile in background:
            #     window.blit(bg_image, tile)
            window.blit(self.bg_image, (0,0))

            for obj in self.objects:
                if not isinstance(obj, Enemy):
                    obj.draw(window, self.offset_x, self.offset_y)

            for enemy in self.enemies:
                if self.enemies_group.has(enemy): #ACA ESTA LA LOGICA PADREEEEEE
                    enemy.draw(window, self.offset_x, self.offset_y)
                    #MAKE THEM DISSAPEAR AFTER DEATH/EXPLOSION ANIMATION
                #TODO: REFACTOR CONDITION TO LOOK FOR SHOOTING ENEMIES
                if enemy.name == "plant":
                    for bullet in enemy.active_bullets:
                        #TODO: THIS LINE MOST LIKELY BUGGING BULLET SPAWN
                        bullet.draw(window, self.offset_x, self.offset_y)

            self.player.draw(window, self.offset_x, self.offset_y)
            for projectile in self.player.projectiles:
                projectile.draw(window, self.offset_x, self.offset_y)

            for item in self.items:
                item.draw(window, self.offset_x, self.offset_y)

        pygame.display.update()