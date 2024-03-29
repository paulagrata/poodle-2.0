from pygame.math import Vector2

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 64
SPEED = 500
FORESTSPEED = 700
WOOZYSPEED = 200

# apple positions
APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

# overlay positions
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (90, SCREEN_HEIGHT - 20),
    'inventory': (145, SCREEN_HEIGHT - 15),
    'seedinventory': (115, SCREEN_HEIGHT - 5),
    'iteminventory': (170, SCREEN_HEIGHT - 5),
    'clock': (750, SCREEN_HEIGHT - 5)   #760
}

# tool hit boxes
PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

# layers for map
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
	'fruit': 9,
    'rain drops': 10,
}

# plant grow speed
GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

# shop prices:
# [sell]
SALE_PRICES = {
    'wood': 4,
    'apple': 4,
    'corn': 10,
    'tomato': 20,
    'corn-seed': 1,
    'tomato-seed': 1,
}
# [buy]
PURCHASE_PRICES = {
    'wood': 5,
    'apple': 6,
    'corn': 20,
    'tomato': 30,
    'corn-seed': 4,
    'tomato-seed': 5,
}


# UI
BAR_HEIGHT = 20
BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
UI_FONT = 'font/LycheeSoda.ttf'
UI_FONT_SIZE = 18

# gennie colors
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = '#F4B9B8'
ENERGY_COLOR = '#41729F'
UI_BORDER_COLOR_ACTIVE = 'gold'

MOOD_COLORS = {
    'health': '#F4B9B8',
    'energy': '#41729F'
}