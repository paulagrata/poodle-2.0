import pygame
from settings import *
from timers import Timer
import json


class Pause:
    def __init__(self, player, clock, toggle_pause):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.clock = clock
        self.toggle_pause = toggle_pause

        # font
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE+5)
        self.color = "BLACK"
        self.text = "Paused"
        self.subtext = "Press ESC to Resume"

        # menu
        self.active = True

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.options = ['save game','load saved game','new game','settings']
        self.sell_border = 5

        # movement
        self.index = 0
        self.timer = Timer(200)
        
        # setup 
        self.setup()

    def setup(self):

        # create the text surfaces
        self.text_surfs = []
        self.total_height =  0

        # boxes
        for index, item in enumerate(self.options):
            display_name = item
            text_surf = self.font.render(display_name, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top,self.width,self.total_height)

        # title
        self.text_surface = self.title_font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (SCREEN_WIDTH // 2, self.menu_top - 30)  # Adjust the y-coordinate to position the text above

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE] and not self.active:
            self.toggle_pause()
        self.active = keys[pygame.K_ESCAPE]
        
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                selected_option = self.options[self.index]
                if selected_option == self.options[0]:  # save
                    print('save game')
                    GameManager.save_game_state(self.player, self.clock)
                elif selected_option == self.options[1]: # load
                    print('load game')
                    game_state = GameManager.load_game("save_file.json")
                    GameManager.import_data(self.player, self.clock, game_state)
                elif selected_option == self.options[2]: # new
                    print('new game')
                elif selected_option == self.options[3]: # settings
                    print('settings')
                        
        # allow scroll to restart
        self.index %= len(self.options)
                        
    def display(self, text_surf, top, selected):

        # title
        self.display_surface.blit(self.text_surface, self.text_rect)

        # background
        bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White',bg_rect, 0, 4)

        # text boxes
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf,text_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface,'black', bg_rect, 4,4)

    def update(self):
        self.input()

        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            self.display(text_surf, top, self.index == text_index)


class GameManager:
    @staticmethod
    def save_game(filename, game_state):
        with open(filename, 'w') as file:
            json.dump(game_state, file)

    @staticmethod
    def save_game_state(player, clock, filename="save_file.json"):

        hours, minutes, seconds = clock.calculate_time()

        game_state = {
            "player_item_inventory": player.item_inventory,
            "player_seed_inventory": player.seed_inventory,
            "player_posx": player.pos.x,
            "player_posy": player.pos.y,
            "player_health": player.health,
            "player_energy": player.energy,
            "player_days": clock.days,
            "player_time": {'hours':hours, 'minutes':minutes, 'seconds':seconds},
        }

        GameManager.save_game(filename, game_state)
        print("Game state saved successfully.")

    @staticmethod
    def load_game(filename):
        with open(filename, 'r') as file:
            game_state = json.load(file)
            return game_state
    
    @staticmethod
    def import_data(player, clock, game_state):
        player.item_inventory = game_state["player_item_inventory"]
        player.seed_inventory = game_state["player_seed_inventory"]
        player.pos.x = game_state["player_posx"]
        player.pos.y = game_state["player_posy"]
        player.health = game_state["player_health"]
        player.energy = game_state["player_energy"]
        clock.days = game_state["player_days"]
        player_time = game_state["player_time"]
        clock.time(player_time["hours"], player_time["minutes"], player_time["seconds"])

