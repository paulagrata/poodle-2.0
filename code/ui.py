import pygame
from settings import *

class UI:
    def __init__(self):

        # general setup
        self.display_surface = pygame.display.get_surface()

        # font
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(790 - BAR_WIDTH ,570,BAR_WIDTH,BAR_HEIGHT)    #l,t,w,h
        self.energy_bar_rect = pygame.Rect(790 - BAR_WIDTH ,546,BAR_WIDTH,BAR_HEIGHT)


    def show_money(self, player):
        self.font = pygame.font.Font(UI_FONT,30)
        text_surf = self.font.render(f'${player.money}', False, 'Black')
        text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 10, 10))

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

        # moods
        moods = ['health', 'energy']        
        for mood in moods:
            if getattr(player, mood) <= 30:
                MOOD_COLORS[mood] = 'Red'

        # mood ui
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, MOOD_COLORS['health'])
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, MOOD_COLORS['energy'])

        # money ui
        self.show_money(player)