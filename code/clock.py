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

        # days
        self.days = 0   
        self.day_incremented = False


    def display(self):

        # time 
        time_str = self.time()
        text_surface = self.font.render(str(time_str), True, (255, 255, 255))  # Render the time as text
        time_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10)) 
        self.display_surface.blit(text_surface, time_rect)


        # day
        day_text_surface = self.font.render(f"Day: {self.days}", True, (255, 255, 255))
        day_text_rect = day_text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 30))
        self.display_surface.blit(day_text_surface, day_text_rect)


    def time(self):
        self.clock.tick() # fps:30

        if self.active:
            self.time_elapsed += 1000 * self.clock.get_time()

        seconds = self.time_elapsed // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60) 
        
        hours += 10 # 10am

        # days
        if hours == 10 and not self.day_incremented:
            self.days += 1
            self.day_incremented = True


        # stops at 3am
        if hours >= 27:
            self.pause()
            return "3 AM"

        # am/pm 
        hours = hours % 24 
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 if hours % 12 != 0 else 12
        
        time_str = "{:2d} {}".format(display_hours, am_pm)
        return time_str
        
    def pause(self):
        self.active = False

    def resume(self):
        self.active = True
