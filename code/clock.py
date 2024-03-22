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
        self.load_time = 0

        # days
        self.days = 0   
        self.day_incremented = False


    def display(self):

        hours, minutes, seconds = self.calculate_time()
        
        # time 
        time_str = self.time(hours, minutes, seconds)
        text_surface = self.font.render(str(time_str), True, (255, 255, 255))  # Render the time as text
        time_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 30)) 
        self.display_surface.blit(text_surface, time_rect)

        # day
        day_text_surface = self.font.render(f"Day: {self.days}", True, (255, 255, 255))
        day_text_rect = day_text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.display_surface.blit(day_text_surface, day_text_rect)


    def calculate_time(self):
        self.clock.tick()

        if self.active:
            self.time_elapsed += 250 * self.clock.get_time()

        seconds = self.time_elapsed // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60) 

        hours += 10 # 10am

        return hours, minutes, seconds

    def time(self, hours, minutes, seconds):
        # day counter
        if hours == 10 and not self.day_incremented:
            self.days += 1
            self.day_incremented = True

        # time stops at 3am
        if hours >= 27:
            self.pause()
            return "3:00 AM"

        hours = hours % 24 
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 if hours % 12 != 0 else 12

        minutes = min(((minutes + 5) // 10) * 10, 50)
        
        time_str = "{:2d}:{:02d} {}".format(display_hours, minutes, am_pm)
        self.load_time = time_str
        return time_str
        
    def pause(self):
        self.active = False

    def resume(self):
        self.active = True
