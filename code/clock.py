import pygame
from settings import *
from timers import Timer 

class Clock:
    def __init__(self) :

        #general setup
        self.display_surface = pygame.display.get_surface()

        #font
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # time
        self.active = True
        self.time_elapsed = 0
        self.clock = pygame.time.Clock()



    def display(self):

        # time 
        time_str = self.time()
        text_surface = self.font.render(str(time_str), True, (255, 255, 255))  # Render the time as text
        time_rect = text_surface.get_rect(midbottom=OVERLAY_POSITIONS['clock'])
        self.display_surface.blit(text_surface, time_rect)


    def time(self):
        self.clock.tick() # fps:30

        if self.active:
            self.time_elapsed += 1000 * self.clock.get_time()

        seconds = self.time_elapsed // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60) 
        hours += 10 # 10am

        # stops at 2am
        if hours >= 26:
            self.pause()
            return "2 AM"

        hours = hours % 24 
        
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 if hours % 12 != 0 else 12

        if hours == 0:
            am_pm = 'AM'
        elif hours >= 12:
            am_pm = 'PM'

        time_str = "{:2d} {}".format(display_hours, am_pm)
        return time_str
        
    def pause(self):
        self.active = False

    def resume(self):
        self.active = True
