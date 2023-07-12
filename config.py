import pygame
from os import listdir
from os.path import isfile, join

### GLOBAL CONSTANTS ###

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000,800
FPS = 60
PLAYER_VEL = 5

### CLASS CONSTANTS ###
block_size = 96
pause_menu_size = 288

### INSTANCES & GROUPS ###


### Helper Funcs. ###

#1. Sprites loading/Handling
pygame.init()
pygame.display.set_mode((WIDTH,HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def normalize_png(png_name: str) -> str:
    return png_name.replace(".png", "").split(" ")[0].lower()

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            #all_sprites[image.replace(".png", "") + "_right"] = sprites
            #all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
            all_sprites[normalize_png(image) + "_right"] = sprites
            all_sprites[normalize_png(image) + "_left"] = flip(sprites)
        else:
            #all_sprites[image.replace(".png", "")] = sprites
            all_sprites[normalize_png(image)] = sprites

    return all_sprites

def load_block(size): #size MUST MATCH block's size in the spritesheet's grid
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96,0, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    
    if image.get_width() > WIDTH and image.get_height() > HEIGHT:
        image = pygame.transform.scale(image, (WIDTH,HEIGHT))

    _, _, width, height = image.get_rect() #params= (x,y,width,height)
    
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j* height)
            tiles.append(pos)
    return tiles, image

#1. Collision Handling


