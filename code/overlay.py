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
        self.inventory_surf = {inventory: pygame.image.load(f'{overlay_path}{inventory}.png').convert_alpha() for inventory in player.inventorys}

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

        #inventory
        inventory_surf = self.inventory_surf[self.player.selected_inventory]
        inventory_rect = inventory_surf.get_rect(midbottom = OVERLAY_POSITIONS['inventory'])
        self.display_surface.blit(inventory_surf,inventory_rect)

        #inventory amount
        item_amount = self.player.item_inventory[self.player.selected_inventory]
        item_amount_surf = self.font.render(f'{item_amount}', False, 'White')
        item_amount_rect = item_amount_surf.get_rect(midbottom = OVERLAY_POSITIONS['iteminventory'])
        self.display_surface.blit(item_amount_surf,item_amount_rect)

        #seed inventory amount
        seed_amount = self.player.seed_inventory[self.player.selected_seed]
        amount_surf = self.font.render(f'{seed_amount}', False, 'White')
        amount_rect = amount_surf.get_rect(midbottom = OVERLAY_POSITIONS['seedinventory'])
        self.display_surface.blit(amount_surf,amount_rect)

    def pause(self):
        self.active = False
        
    def resume(self):
        self.active = True
