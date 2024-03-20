import pygame
from settings import *

class Notification:
    def __init__(self, toggle_notification, text):
        
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.toggle_notification = toggle_notification

        # font
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.color = "BLACK"
        self.text = text
        self.subtext = "press X to close"

        # setup 
        self.active = True
        self.setup()

    def setup(self):
        # font
        self.text_surf = self.font.render(self.text, False, 'Black')
        self.subtext_surf = self.font.render(self.subtext, False, 'Black')
        # position 
        self.text_rect = self.text_surf.get_rect(bottomright=(self.display_surface.get_width() - 15, self.display_surface.get_height() - 130))
        self.subtext_rect = self.subtext_surf.get_rect(bottomright=(self.display_surface.get_width() - 15, self.display_surface.get_height() - 110))
        # combines in one box
        self.text_and_subtext_rect = self.text_rect.union(self.subtext_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            self.toggle_notification(text='')

    def display(self):
        pygame.draw.rect(self.display_surface, 'White', self.text_and_subtext_rect.inflate(10, 10), 0, 6)
        self.display_surface.blit(self.text_surf, self.text_rect)
        self.display_surface.blit(self.subtext_surf, self.subtext_rect)
            
    def update(self):
        self.input()
        self.display()