import pygame

class BaseLevel:
    def __init__(self):
        self.enemies = None
        self.objects = None
        self.platforms = None
        self.finished = False
        self.level_number = 0
        #self.player = Player()
        #self.screen = Screen()
        #self.score = Scoreboard()
        #self.soundtrack = SoundTrack()
        #self.timer = Timer()
        #self.gameover = GameOverScreen()
        #self.font = FontManager().get_default_font()
        self.is_paused = True
        #self.clock = Clock()
        #self.fps = FPSMeter()
        #self.current_time = time.perf_counter()
        self.previous_frame_time = -1
        self.last_update = 0
        self.delta_t = 0
        self.total_frames = 0
        self.max_fps = 60
        self.min_fps = 35
        self.target_fps = (self.max_fps + self.min_fps)
        self.average_fps = int((self.max_fps+self.min_fps)/2)
        #self.fps_meter = FPSCounter(self.max_fps, self.min_fps, self.average_fps)
        # end region

    def draw_background(self, screen):
        pass
    
    def create_platform(self):
        pass

    def init_entities(self):
        pass

    def spawn_random_items(self):
        pass

    def control_traps(self):
        pass

    def trigger_traps(self):
        pass
    
    def is_finished(self):
        pass