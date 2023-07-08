#import os, random, math
import pygame
from config import *
from items import *
from player import *
from obj import *
from enemy import *
from menu import *
from traps import *

pygame.init()

pygame.display.set_caption("Super Pixel boys")

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.get_wm_info()

def draw(window, background, bg_image, player, objects, enemies, offset_x, offset_y, scroll, groups, items, menus):
    if any(menu.is_active for menu in menus):
        for menu in menus:
            if menu.is_active:
                menu.draw(window)
                break
    else:
        for tile in background:
            window.blit(bg_image, tile)

        for obj in objects:
            if not isinstance(obj, Enemy):
                obj.draw(window, offset_x, offset_y)
            #obj.draw(window, scroll)

        for enemy in enemies:
            if groups[0].has(enemy): #ACA ESTA LA LOGICA PADREEEEEE
                enemy.draw(window, offset_x,offset_y)
                #MAKE THEM DISSAPEAR AFTER DEATH/EXPLOSION ANIMATION
            #enemy.draw(window, scroll)
            #TODO: REFACTOR CONDITION TO LOOK FOR SHOOTING ENEMIES
            if enemy.name == "plant":
                for bullet in enemy.active_bullets:
                    bullet.draw(window, offset_x,offset_y)

        player.draw(window, offset_x,offset_y)
        for projectile in player.projectiles:
            projectile.draw(window, offset_x,offset_y)
        #player.draw(window, scroll)

        for item in items:
            item.draw(window, offset_x,offset_y)

    pygame.display.update()


def handle_vertical_collision(player, objects, player_y_vel):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if player_y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player_y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            #
            collided_objects.append(obj)
    return collided_objects

##################
def handle_vertical_collision_group(player, objects_group, player_y_vel):
    #collided_objects = []
    collided_objects = pygame.sprite.spritecollide(player, objects_group, False)
    if collided_objects:
        for obj in collided_objects:
            #if pygame.sprite.collide_mask(player, obj):
            if player_y_vel > 0:
                if not isinstance(obj, Enemy):
                    player.rect.bottom = obj.rect.top
                    player.landed()
                else:
                    if obj and player.rect.bottom <= obj.rect.top and obj.name == "bunny" and not player.hit:
                        obj.get_hit()
                        print("HIT BUNNY ON TOP 2")
            elif player_y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            #collided_objects.append(obj)
    return collided_objects
##################

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object

##################
def collide_group(player, objects_group, dx):
    player.move(dx, 0)
    player.update()
    #collided_objects = None
    collided_objects = pygame.sprite.spritecollide(player, objects_group)
    # for obj in objects_group:
    #     if pygame.sprite.collide_mask(player, obj):
    #         collided_objects = obj

            #break
    player.move(-dx, 0)
    player.update()
    return collided_objects
##################

def handle_move(player: Player, objects, enemies_group):
    keys = pygame.key.get_pressed()

    player.x_vel = 0 #This way no flag is needed to know if player is moving
    
    collide_left = collide(player, objects, -PLAYER_VEL *2)
    collide_right = collide(player, objects, PLAYER_VEL *2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)

    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check: #get_trap_names() List to replace "fire"
        
        if obj and isinstance(obj, Block):
            player.attatch_to_wall(obj)
            #print(f'attached?: {player.attached}')
        
        if obj and obj.name == "fire" and obj.animation_name == "on" and not player.hit:
            player.get_hit()
            print("COLLIDING WITH FIRE")
            #player.lose_life()

        if obj and isinstance(obj, Enemy) and player.rect.bottom <= obj.rect.top:
            obj.get_hit()
            player.jump(player.JUMP_POWER/2)
            print("HIT ENEMY ON TOP")
            print(f'lives:{obj.lives}')
            if not obj.alive:
                objects.remove(obj) #TODO:ANIMATE DEATH AS WELL!!!
                obj.kill() #


            break

        elif obj and isinstance(obj, Enemy) and not player.hit and not obj.hit:
            player.get_hit()

            #player.lose_life()


def main(window): ######## MAIN LOOP ########
    clock = pygame.time.Clock()
    background, bg_image = get_background("Sky_wall.jpg")

    #True Scroll variable
    true_scroll = [0,0]

    # Creating a main menu instance & menus list
    menus_list = []
    main_menu = MainMenu(0,0, True)
    pause_menu_size = 288
    pause_menu = PauseMenu((WIDTH//2-pause_menu_size/2), (HEIGHT//2-pause_menu_size*3/5), False, [main_menu])
    menus_list.extend([main_menu, pause_menu])

    # Creating Groups for all the different sprites
    all_sprites = pygame.sprite.Group()

    platforms_group: pygame.sprite.Group()

    player_group = pygame.sprite.GroupSingle()
    
    enemies_group = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    objects_group = pygame.sprite.Group()


    #SEND TO CONSTANTS
    block_size = 96
    BUNNY_HEIGHT = 88 #WHY TF IS IT DOUBLE THE SIZE?

    player = Player(100,100, 50, 50)
    player_group.add(player)

    fire = Fire(250, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i* block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH*2 // block_size)]
    
    ##TODO: ITEMS GROUP -> MOVE TO JSON / LEVEL METHOD TO CREATE OBJS.
    apple = Item(400, HEIGHT - block_size - 64, 32, 32, "apple")
    bananas = Item(450, HEIGHT - block_size - 64, 32, 32, "bananas")
    cherries = Item(500, HEIGHT - block_size - 64, 32, 32, "cherries")
    bomb = Item(550, HEIGHT - block_size - 64, 32, 32, "bomb_2")
    one_up = Item(600, HEIGHT - block_size - 64, 32, 32, "1up")
    heart = Item(670, HEIGHT - block_size - 64, 32, 32, "heart")
    coin = Item(750, HEIGHT - block_size - 64, 32, 32, "coin")


    items_group = pygame.sprite.Group([apple,bananas, cherries, bomb, one_up, heart,coin])

    air_platform = [Block(i* block_size, HEIGHT - block_size*4, block_size) for i in range((WIDTH - 300) // block_size, WIDTH // block_size)]
    
    objects_group.add(fire, *floor, *air_platform)

    #NOTE: on_floor() helper func. to calc y coordinate for a sprite to be on top of main floor
    enemies = [Bunny(700, HEIGHT-block_size-BUNNY_HEIGHT,34,44),
               Plant(800,HEIGHT-block_size*4-84, 44, 42)]

    enemies_group.add(*enemies)

    objects = [*floor, Block(0,HEIGHT - block_size*2, block_size),
               Block(block_size*3,HEIGHT-block_size*4, block_size), fire, *enemies,*air_platform]

    objects_group.add(objects[31], objects[32]) #REFACTOR THIS CRAP 
    
    all_sprites.add(player, fire, *floor, *air_platform, *enemies) #TODO:
    
    offset_x = 0
    offset_y = 0
    scroll_area_width = 150

    #Fluffly scrolling / Parallax
    true_scroll[0] += (player.rect.x-true_scroll[0]-(WIDTH//2 + player.rect.width//2))/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-(HEIGHT//2+player.rect.height//2))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #############################

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if main_menu.is_active:
                        running = False
                        pygame.quit()
                        exit()
                    elif not pause_menu.is_active:
                        pause_menu.is_active = True
                    else:
                        pause_menu.is_active = False

                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    if not player.attached:
                        player.jump()
                    else:
                        if player.direction == "right":
                            player.x_vel -= 15
                        else:
                            player.x_vel += 15
                        player.jump()

                if event.key == pygame.K_LSHIFT and not player.dashing:
                    player.dash()
                if event.key == pygame.K_LCTRL:
                    player.throw_projectile()
                    #TODO: CLEAR PROJECTILES LIST

        ### Updating and looping ALL ###

        main_menu.update()
        pause_menu.update()

        player.loop(FPS)

        if player.check_fall():
            offset_x, offset_y = player.x, player.y

        fire.loop()
        items_group.update()

        #TO LEVEL LOGIC
        for enemy in enemies: 
            enemy.loop()
            if enemy.name == "plant" and enemy.alive:
                enemy.shoot(offset_x, player)
                #TODO: FIX BULLETS OFFSET_X TO MATCH PLANT's X POS.
                if enemy.active_bullets:
                    if pygame.sprite.spritecollide(player, enemy.active_bullets, True):
                        player.get_hit()

        #TO BULLET LOGIC (OR PLAYER CLASS LOGIC MAYBE?)
        for bomb in player.projectiles:

            for obj in objects_group:
                if pygame.sprite.collide_mask(bomb, obj):
                    print(f'collided w/ {obj}')
                    player.projectiles.remove(bomb)
                    break

            for enemy in enemies_group:
                if pygame.sprite.collide_mask(bomb, enemy):
                    print(f'collided with {type(enemy)}')
                    
                    #TODO:REFACTOR THIS LOGIC TO SOME FUNC/METHOD
                    enemy.get_hit() 
                    player.projectiles.remove(bomb)
                    if not enemy.alive:
                        enemies_group.remove(enemy)
                        objects.remove(enemy) #TODO:ANIMATE DEATH AS WELL!!!
                        enemy.kill() #
            
        items_collision = pygame.sprite.spritecollide(player, items_group, False)
        for item in items_collision:
            if not item.grabbed:
                item.grabbed = True
                player.grab_item(item)
                print(f"COLLISION w/ {item.name}")


        # for item in items_group:
        #     if pygame.sprite.collide_mask(player, item):
        #         print("ITEM MASK COLLIDED")

                    #enemies.remove(enemy) # 
                    # ADD ALL SPRITES TO A GROUP
                    # REFACTOR DRAW / DIRECTLY DRAW SPRITE GROUPS
                    # UPDATE ALL SPRITES GROUPS

        handle_move(player, objects, enemies_group)
        draw(window, background, bg_image, player, objects, enemies, offset_x, offset_y, scroll, [enemies_group], items_group, menus_list)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_width) and player.y_vel > 0) or (
            (player.rect.top - offset_y <= scroll_area_width) and player.y_vel < 0):
            offset_y += player.y_vel

    pygame.quit() #quitting pygame module
    quit() #quitting python program

########### MAIN EXECUTION ###########
if __name__ == "__main__":
    main(window)