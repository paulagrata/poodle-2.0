import pygame
from settings import *

class UI:
    def __init__(self):

        # general setup
        self.display_surface = pygame.display.get_surface()

        # font
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)    #l,t,w,h
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)


    def show_money(self, player):
        text_surf = self.font.render(f'${player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10),0,6) # 0,6 rounds it.

        self.display_surface.blit(text_surf,text_rect)

    def show_bar(self,current, max_amount, bg_rect, color):

        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width =  bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,bg_rect,3)
        

    def display(self, player):
        #pygame.draw.rect(self.display_surface,'black',self.health_bar_rect)

        # mood ui
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        # money ui
        self.show_money(player)