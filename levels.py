import copy
import pygame
from config import *

from obj import Block

class Level:
    def __init__(self, name, level_number, terrain, player, enemies, enemies_group, traps, platforms, coins, fruits, lifes, timer, menus, next_level, unlocked): #replace items w/ a JSON
        self.name = name
        self.terrain = terrain
        self.player = player
        self.enemies = enemies
        self.enemies_group = enemies_group
        self.platforms = platforms
        self.traps = traps
        self.items = self.spawn_random_items(coins, fruits, lifes)
        self.pause_menu = menus["pause"]
        self.endlevel_menu = menus["endlevel"]
        self.game_over_menu = menus["game_over"]
        self.paused = False
        self.finished = False
        self.is_active = False
        self.timer = timer
        self.level_number = level_number
        self.next_level = next_level
        self.unlocked = unlocked
        self.save_initial_entities()

        self.offset_x = 0
        self.offsext_y = 0
        self.scroll_area_width = 150

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

    def spawn_random_items(self, coins, fruits, lifes, amount):
        pass

    def draw_player_lives(self):
        pass

    def pause(self):
        if not self.paused:
            self.paused = True

    def show_endlevel_menu(self):
        if self.finished:
            pass

    def init_entities(self, player, enemies, traps, platforms):
        pass

    def save_initial_entities(self):
        self.original_terrain = copy.deepcopy(self.terrain)
        self.original_player = copy.deepcopy(self.player)
        self.original_enemies = copy.deepcopy(self.enemies)
        self.original_traps = copy.deepcopy(self.traps)
        self.original_platforms = copy.deepcopy(self.platforms)
        self.original_coins = copy.deepcopy(self.coins)
        self.original_fruits = copy.deepcopy(self.fruits)

    def reset_entities(self):
        self.terrain = copy.deepcopy(self.original_terrain)
        self.player = copy.deepcopy(self.original_player)
        self.enemies = copy.deepcopy(self.original_enemies)
        self.traps = copy.deepcopy(self.original_traps)
        self.platforms = copy.deepcopy(self.original_platforms)
        self.coins = copy.deepcopy(self.original_coins)
        self.fruits = copy.deepcopy(self.original_fruits)

    def restart_level(self):
        for button in self.pause_menu.buttons:
            if button.name == "restart" and button.clicked:
                self.reset_entities()


    def animate_background(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        if self.is_active and not self.paused and not self.finished:
            pass
    
    def create_platform(self, height_multiplier, start, end):
        return [Block(i* block_size, HEIGHT - block_size*height_multiplier, block_size) for i in range(start // block_size, end // block_size)]


    def control_traps(self):
        pass

    def trigger_traps(self):
        pass

    def disable_traps(self):
        pass
    
    def is_finished(self):
        if not self.finished:
            self.finished = True
    
    def draw_all(self, win):
        #move draw() function from main to here
        pass