import pygame

class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def get_elapsed_time(self):
        if self.active:
            return pygame.time.get_ticks() - self.start_time
        else:
            return 0

    def update(self):
        if self.active and pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func:
                self.func()
            self.deactivate()