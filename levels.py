import pygame

class BaseLevel:
    def __init__(self, name, level_number, player, enemies, traps, platforms, coins, fruits, lifes, timer): #replace items w/ a JSON
        self.name = name
        self.player = player
        self.enemies = enemies
        self.platforms = platforms
        self.traps = traps
        self.items = self.spawn_random_items(coins, fruits, lifes)
        self.paused = False
        self.finished = False
        self.timer = timer
        self.level_number = level_number

    def draw_player_lives(self):
        pass

    def pause(self):
        if not self.paused:
            self.paused = True

    def show_endlevel_menu(self):
        pass

    def restart_level(self):
        pass

    def draw_background(self, win):
        pass

    def init_entities(self, player, enemies, traps, platforms):
        pass

    def spawn_random_items(self, coins, fruits, lifes):
        pass

    def handle_events(self):
        pass

    def update(self):
        if not self.paused:
            pass
    
    def create_platform(self):
        pass

    def control_traps(self):
        pass

    def trigger_traps(self):
        pass
    
    def is_finished(self):
        if not self.finished:
            self.finished = True
    
    def draw_all(self, win):
        #move draw() function from main to here
        pass