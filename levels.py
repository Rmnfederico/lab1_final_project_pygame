import pygame

class BaseLevel:
    def __init__(self):
        pass

    def draw_background(self, screen):
        pass
    
    def create_platform(self):
        pass

    def init_entities(self):
        pass
    
    def control_traps(self):
        pass

    def trigger_traps(self):
        pass
    
    def is_finished(self):
        pass