import pygame
from settings import *

class Overlay:
    def __init__(self, player):

        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # pause
        self.paused = False
        self.pause_start_time = 0
        self.start_time = pygame.time.get_ticks()

        #imports [key value pairs, not same as tools/seeds used]
        overlay_path = 'graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}
        #print(self.tools_surf)
        #print(self.seeds_surf)

        #font
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)


    def display(self):

        #tool
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf,tool_rect)

        #seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf,seed_rect)


        if not self.paused:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.pause_start_time) * 500

            minutes = (elapsed_time // (1000 * 60)) % 60
            hours = 10 + (elapsed_time // (1000 * 60 * 60)) % 24

            if hours == 0: time_str = f"12:{minutes:02} AM"  # [midnight] f"Time: 12:{minutes:02} AM" 
            elif hours < 12: time_str = f"{hours:02}:{minutes:02} AM"  #f"Time: {hours:02}:{minutes:02} AM"
            elif hours == 12: time_str = f"12:{minutes:02} PM"  # [noon]
            else: time_str = f"{hours-12:02}:{minutes:02} PM"

            text_surface = self.font.render(time_str, True, (255, 255, 255))  # Render the time as text
            time_rect = text_surface.get_rect(midbottom=OVERLAY_POSITIONS['clock'])
            self.display_surface.blit(text_surface, time_rect)


    def pause(self):
        self.paused = True


    def resume(self):
        self.paused = False
