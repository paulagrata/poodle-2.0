import pygame
from settings import *
from timers import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, 30)    #(font, size)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

         
    def display_options(self):
        text_surf = self.font.render('Buy press X, Sell press S', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

        #pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10),0,6) # 0,6 rounds it.

        self.display_surface.blit(text_surf,text_rect) 
    

    def setup(self):

        # create the text surfaces
        self.text_surfs = []
        self.total_height =  0

        for index, item in enumerate(self.options):
            if index > self.sell_border:  # if buy item
                display_name = f"{item[:-5]} seed"
            else:
                display_name = item
            

            text_surf = self.font.render(display_name, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top,self.width,self.total_height)

        # buy / sell text surface
        self.buy_text = self.font.render('buy',False,'Black')
        self.sell_text = self.font.render('sell',False,'Black')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()
        
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            # sell
            if keys[pygame.K_s]:
                self.timer.activate()
                current_item = self.options[self.index]
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
                else:  # Selling seeds
                    if self.player.seed_inventory[current_item] > 0:
                        self.player.seed_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
            # buy
            if keys[pygame.K_x]:
                self.timer.activate()
                current_item = self.options[self.index]

                print(self.index)
                print(self.sell_border)

                if self.index <= self.sell_border:
                    price = PURCHASE_PRICES[current_item]
                    if self.player.money >= price:
                        self.player.item_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]
                else: 
                    price = PURCHASE_PRICES[current_item]
                    if self.player.money >= price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]
                        
        #clamo the values
        self.index %= len(self.options)
                        
    def show_entry(self, text_surf, amount, top, selected):

        # background
        bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White',bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf,text_rect)

        # current item
        for text_index, item in enumerate(self.options):
            if text_surf == self.text_surfs[text_index]:
                current_item = item
                break

        # sell
        current_item = self.options[text_index]  
        if text_index <= self.sell_border: 
            price_surf = self.font.render('$'+str(SALE_PRICES[current_item]), False, 'Black')
        # buy
        else:
            price_surf = self.font.render('$'+str(PURCHASE_PRICES[current_item]), False, 'Black')
        price_rect = price_surf.get_rect(midright = (self.main_rect.right - 50, bg_rect.centery))
        self.display_surface.blit(price_surf,price_rect)


        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf,amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface,'black', bg_rect, 4,4)
            if self.index <= self.sell_border:   # sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.right - 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text,pos_rect)
            else:  
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.right - 150, bg_rect.centery))                             # buy
                self.display_surface.blit(self.buy_text,pos_rect)
    
    def update(self):
        self.input()
        self.display_options()
        

        #pygame.draw.rect(self.display_surface,'pink',self.main_rect)
        #self.display_surface.blit(pygame.Surface((500,500)),(0,0)) # black rect

        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)

            #self.display_surface.blit(text_surf,(100, text_index * 50))