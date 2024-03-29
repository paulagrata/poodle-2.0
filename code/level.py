import pygame
from settings import *
from player import Player
from overlay import Overlay
from clock import Clock
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu
from ui import UI
from stats import StatUpdater
from pause import Pause, GameManager
from notification import Notification


class Level:
    def __init__(self):

        # get the display surface.
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups
        #self.all_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        
        self.setup(all_sprites=self.all_sprites)
        self.overlay = Overlay(self.player)
        
        self.transition = Transition(self.reset,self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0,10) > 7 #true: on, false: off
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # clock
        self.clock = Clock()

        # ui
        self.ui = UI()
        self.stats = StatUpdater(self.player, self.clock)

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # pause 
        self.paused = Pause(self.player, self.clock, self.toggle_pause)
        self.pause_active = False

        # notifications
        self.notification = Notification(self.toggle_notification, text='')
        self.notification_active = False

        # music
        self.success = pygame.mixer.Sound('audio/success.wav')
        self.success.set_volume(0.1)
        self.music = pygame.mixer.Sound('audio/sprouting.mp3')
        self.music.play(loops = -1).set_volume(0.2)
        
    def setup(self, all_sprites):
        tmx_data = load_pygame('data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # fence 
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])
        
        # water 
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # trees 
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos = (obj.x, obj.y), 
                surf = obj.image, 
                groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
                all_sprites = all_sprites, 
                name = obj.name,
                player_add = self.player_add
                )

        # wildflowers     
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x,obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # collion tiles     
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), [self.collision_sprites])

        # player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x,obj.y), 
                    group = [self.all_sprites], 
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites,
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    toggle_shop = self.toggle_shop,
                    toggle_pause= self.toggle_pause,
                    toggle_notification = self.toggle_notification)
                
            if obj.name == 'Bed':
                Interaction(
                    pos = (obj.x, obj.y), 
                    size = (obj.width, obj.height), 
                    groups = self.interaction_sprites, 
                    name = obj.name)
                
            if obj.name == 'Trader':
                Interaction(
                    pos = (obj.x, obj.y), 
                    size = (obj.width, obj.height), 
                    groups = self.interaction_sprites, 
                    name = obj.name)


        Generic(
            pos = (0,0), 
            surf = pygame.image.load('graphics/world/ground.png').convert_alpha(), 
            groups = self.all_sprites,
            z = LAYERS['ground']
            )

    def player_add(self,item):
        self.player.item_inventory[item] += 1
        self.success.play()

    def toggle_notification(self, text):
        self.notification = Notification(self.toggle_notification, text)
        self.notification_active = not self.notification_active #switching on and off.

    def toggle_pause(self):
        self.pause_active = not self.pause_active #switching on and off.

    def toggle_shop(self):
        self.shop_active = not self.shop_active #switching on and off.

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(
                        pos = plant.rect.topleft, 
                        surf = plant.image, 
                        groups = self.all_sprites, 
                        z = LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')   # row y of plant ,column x of plant

    def reset(self):

        # plants [must be called before soil/rain]
        self.soil_layer.update_plants()

        # soil
        self.soil_layer.remove_water()

        # randomize the rain
        self.raining = randint(0,10) > 7 
        self.soil_layer.raining = self.raining
        if self.raining:
            # waters soil if raining
            self.soil_layer.water_all()
        
        # apples on the trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit(self.all_sprites)

        # sky
        self.sky.start_color = [255,255,255]

        # clock
        self.clock.time_elapsed = 0
        self.clock.get_time = 0
        self.clock.day_incremented = False

        self.stats.reset()
        self.ui.reset(self.player)

    def pause(self):
        self.clock.pause()
        self.overlay.pause()
        self.sky.pause()
        self.stats.pause()

    def resume(self):
        self.clock.resume()
        self.overlay.resume()
        self.sky.resume()
        self.stats.resume()

    def run(self,dt):

        # drawing logic
        self.display_surface.fill('#9CD5C3')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)

        #UI
        self.overlay.display()
        self.ui.display(self.player)

        # pause
        if self.pause_active:
            self.paused.update()
            self.pause()
        # shop
        elif self.shop_active:
            self.pause()
            self.paused.active = False
            self.menu.update()
        # nothing open: [normal]
        else:
            self.resume()
            self.all_sprites.update(dt, self.all_sprites)
            self.plant_collision()

        # notifications
        if self.notification_active:
            self.notification.update()
        
        # weather 
        if self.raining and not self.shop_active and not self.pause_active:   # rain
            self.rain.update(dt, self.all_sprites)
        
        # daytime 
        self.sky.display(dt)                        

        # transition overlay
        if self.player.sleep:
            self.transition.play()

        # clock
        self.clock.display()

        # testing [debug]:
        #print(self.player.item_inventory)      # prints player's inventory
        #print(self.player.seed_inventory)      # prints player's seed inventory
        #print(self.shop_active)                 # prints if shop is active
        #print('health: ', self.player.health)
        #print('energy: ', self.player.energy)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        #if player moves left, camera moves right
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    #offset_rect = sprite.image.get_rect()
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # shows players hitbox [for debugging]
                    '''
                    if sprite == player:
                        pygame.draw.rect(self.display_surface,'red',offset_rect,5)
                        hitbox_rect = player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
                        target_pos =  offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        pygame.draw.circle(self.display_surface,'blue',target_pos,5)
                    '''