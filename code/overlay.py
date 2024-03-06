import pygame
from settings import *
from timers import Timer 

class Overlay:
    def __init__(self, player):

        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        #imports [key value pairs, not same as tools/seeds used]
        overlay_path = 'graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}
        #print(self.tools_surf)
        #print(self.seeds_surf)

        #font
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # time
        self.active = True
        self.time_elapsed = 0
        self.clock = pygame.time.Clock()



    def display(self):

        #tool
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf,tool_rect)

        #seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf,seed_rect)

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


        
        hours = hours % 24  # Add the elapsed hours and keep within 24 hours
        
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 if hours % 12 != 0 else 12

        if hours == 0:
            am_pm = 'AM'
        elif hours >= 12:
            am_pm = 'PM'


        time_str = "{:2d} {}".format(display_hours, am_pm)
        return time_str
        


    def pause(self):
        #print("Paused the clock")
        self.active = False


    def resume(self):
        self.active = True
