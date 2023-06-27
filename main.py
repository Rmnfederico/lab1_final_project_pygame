#import os, random, math
import pygame
from config import *
from player import *
from obj import *
from enemy import *

pygame.init()

pygame.display.set_caption("Super Pixel boys")

window = pygame.display.set_mode((WIDTH,HEIGHT))

def draw(window, background, bg_image, player, objects, enemies, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    for enemy in enemies:
        enemy.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()

def handle_vertical_collision(player, objects, player_y_vel):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if player_y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
                if isinstance(obj, Enemy):
                    print("ON TOP OF ENEMY")
            elif player_y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            #
            collided_objects.append(obj)
    return collided_objects

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

def handle_move(player: Player, objects):
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
    
    for obj in to_check:
        if obj and obj.name == "fire" and obj.animation_name == "on":
            player.get_hit()
            player.lose_life()
        #
        if obj and obj.name == "bunny" and not player.hit:
            player.get_hit()
            player.lose_life()

        if obj and obj.name == "plant" and not player.hit:
            player.get_hit()
            player.lose_life()

def main(window): ######## MAIN LOOP ########
    clock = pygame.time.Clock()
    background, bg_image = get_background("Sky_wall.jpg")
    #window.blit(bg_image, bg_image_rect)

    # Creating Groups for all the different sprites
    all_sprites = pygame.sprite.Group()

    player_group = pygame.sprite.GroupSingle()
    player_bullets = pygame.sprite.Group()
    
    enemies_group = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    #SEND TO CONSTANTS
    block_size = 96
    BUNNY_HEIGHT = 88 #WHY TF IS IT DOUBLE THE SIZE?

    player = Player(100,100, 50, 50)
    player_group.add(player)

    fire = Fire(150, HEIGHT - block_size - 64, 16, 32)
    #fire.on()
    floor = [Block(i* block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH*2 // block_size)]

    air_platform = [Block(i* block_size, HEIGHT - block_size*4, block_size) for i in range((WIDTH - 300) // block_size, WIDTH // block_size)]
    
    #NOTE: on_floor() helper func. to calc y coordinate for a sprite to be on top of main floor
    enemies = [Bunny(700, HEIGHT-block_size-BUNNY_HEIGHT,34,44),
               Plant(800,HEIGHT-block_size*4-84, 44, 42)]

    objects = [*floor, Block(0,HEIGHT - block_size*2, block_size),
               Block(block_size*3,HEIGHT-block_size*4, block_size), fire, *enemies,*air_platform]

    offset_x = 0
    scroll_area_width = 150

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_LSHIFT and not player.dashing:
                    player.dash()
        
        ### Updating and looping ALL ###

        player.loop(FPS)
        fire.loop()
        
        for enemy in enemies: 
            enemy.loop()
            if enemy.name == "plant":
                enemy.shoot(offset_x)
                if enemy.active_bullets:
                    if pygame.sprite.spritecollide(player, enemy.active_bullets, True):
                        player.get_hit()

        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, enemies, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit() #quitting pygame module
    quit() #quitting python program

########### MAIN EXECUTION ###########
if __name__ == "__main__":
    main(window)