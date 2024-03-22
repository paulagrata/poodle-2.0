import pygame
from settings import *
from support import *
from timers import Timer
from stats import StatUpdater
from clock import Clock

# pos - position

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, toggle_pause, toggle_notification):
        super().__init__(group)

        self.escape_pressed = False 

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index] # uses char images
        #self.image = pygame.Surface((32,64)) # original character = green box
        #self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']

        #movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        #self.speed = 500  # normal: 200

        # collision
        self.hitbox = self.rect.copy().inflate((-126,-70)) # width, length
        self.collision_sprites = collision_sprites

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
            'inventory switch': Timer(200),
            'eat': Timer(350, self.eat),
        }

        # tools
        self.tools = ['hoe','axe','water']
        self.tool_index = 0
        #self.selected_tool = 'axe'
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn-seed', 'tomato-seed']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # player inventory
        self.inventorys = ['wood', 'apple', 'corn', 'tomato']
        self.inventory_index = 0
        self.selected_inventory = self.inventorys[self.inventory_index]
        # items
        self.item_inventory = {
            'wood':   0,
            'apple':  5,
            'corn':   0,
            'tomato': 0
        }
        # seeds
        self.seed_inventory = {
            'corn-seed':   2,
            'tomato-seed': 0
        }
        # money
        self.money = 200

        # stats
        self.stats = {'health': 100, 'energy': 100, 'speed': SPEED}
        self.health = self.stats ['health'] 
        self.energy = self.stats ['energy']
        self.speed = self.stats ['speed']
        clock = Clock() 
        self.stat_updater = StatUpdater(self, clock) 


        # interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop
        self.toggle_pause = toggle_pause
        self.toggle_notification = toggle_notification

        # sounds
        self.watering = pygame.mixer.Sound('audio/water.mp3')
        self.watering.set_volume(0.1)
        self.eating = pygame.mixer.Sound('audio/eat.mp3')
        self.eating.set_volume(0.1)
        self.wood = pygame.mixer.Sound('audio/wood.mp3')
        self.wood.set_volume(0.1)
        
    def use_tool(self):
        #print(self.selected_tool)

        if self.selected_tool == 'hoe':
            if self.soil_layer.get_hit(self.target_pos):
                self.energy -= .5

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    self.energy -= .5
                    tree.damage(self.groups()[0])
            
        if self.selected_tool == 'water':
            if self.soil_layer.water(self.target_pos):
                self.watering.play()
                self.energy -= .2

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def eat(self):
        if self.item_inventory[self.selected_inventory] > 0:
            if self.health < 100:
                self.item_inventory[self.selected_inventory] -= 1
                if self.selected_inventory == "wood":
                    self.health -= 5
                    self.wood.play()
                    self.toggle_notification(text= "wood isn't very good....")
                else:
                    self.health += 5
                    self.eating.play()

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            if self.soil_layer.plant_seed(self.target_pos, self.selected_seed):
                self.seed_inventory[self.selected_seed] -= 1
                self.energy -= .5

    def import_assets(self):
        self.animations = {
            'up': [], 'down' : [], 'left': [], 'right' : [],
            'up_idle': [], 'down_idle' : [], 'left_idle': [], 'right_idle' : [],
            'up_hoe': [], 'down_hoe' : [], 'left_hoe': [], 'right_hoe' : [],
            'up_axe': [], 'down_axe' : [], 'left_axe': [], 'right_axe' : [],
            'up_water': [], 'down_water' : [], 'left_water': [], 'right_water' : [],
        }

        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)

    def animate(self,dt):
        #self.frame_index += 4 * dt
        #if self.frame_index >= len(self.animations[self.status]):
            #self.frame_index = 0 #returns back to 0 to loop animation

        self.frame_index = (self.frame_index+dt*4) % len(self.animations[self.status])

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_ESCAPE] and not self.escape_pressed: 
            # paused
            self.toggle_pause()
            self.escape_pressed = True 
        elif not keys[pygame.K_ESCAPE]: 
            # resumed
            self.escape_pressed = False 
        
        if not self.timers['tool use'].active and not self.sleep:
			# directions 
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
        
            # tool use
            if keys[pygame.K_SPACE]:
                # timer for the tool use
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change tool [list index out of range need timer - only adds one not continously]
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                # need to restart at first tool
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_f]:
                # timer for the tool use
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                #print('use seed')

            # eat
            if keys[pygame.K_b]:
                # timer for the tool use
                self.timers['eat'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                #print('use seed')

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                # need to restart at first seed
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]
                #print(self.selected_seed)

            # change inventory
            if keys[pygame.K_g] and not self.timers['inventory switch'].active:
                self.timers['inventory switch'].activate()
                self.inventory_index += 1
                self.inventory_index = self.inventory_index if self.inventory_index < len(self.inventorys) else 0
                self.selected_inventory = self.inventorys[self.inventory_index]

            # trader
            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction,False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()
                    else:
                        self.status = 'left_idle'
                        self.sleep = True

            # cheats
            if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL] and keys[pygame.K_c]:
                self.stat_updater.reset()
                self.stat_updater.player.health = 100
                print('cheater')

            # run FASTAAAAA
            if keys[pygame.K_LSHIFT]:
                self.speed = FORESTSPEED
                print('RUN FOREST')
            else:
                if self.energy <= 30:
                    self.speed = WOOZYSPEED
                else:
                    self.speed = SPEED

    def get_status(self):
        #if player is not moving = set idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            #print('tool in use')
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
            
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                        
                    if direction == 'vertical':
                        if self.direction.y > 0: # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):

        # normalizing a vector [making sure vector is always 1, length cannot be 0] 
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        #horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx =  round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        #vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery =  round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
            
        #self.pos += self.direction * self.speed * dt
        #self.rect.center = self.pos GRRRRRRRRRRRRRRR

    def update(self, dt, all_sprites):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.stat_updater.update()
        self.move(dt)
        self.animate(dt)