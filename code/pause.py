import pygame
from settings import *

class Pause:
    def __init__(self, toggle_pause):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.toggle_pause = toggle_pause

        # font
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.color = "BLACK"
        self.text = "Paused"
        self.subtext = "Press ESC to Resume"

        # menu
        self.active = True
        
        # setup 
        self.setup()

    def setup(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        self.subtext_surface = self.font.render(self.subtext, True, self.color)
        self.subtext_rect = self.subtext_surface.get_rect()
        self.subtext_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
      
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and not self.active:
            self.toggle_pause()
        self.active = keys[pygame.K_ESCAPE] 

    def display(self):
        self.display_surface.blit(self.text_surface, self.text_rect)
        self.display_surface.blit(self.subtext_surface, self.subtext_rect)
    
        
    def update(self):
        self.input()
        self.display()