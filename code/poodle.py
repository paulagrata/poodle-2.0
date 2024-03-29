import pygame, sys
import importlib
from settings import *
import settings
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Poodle')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            dt = self.clock.tick(300) / 1000        #fps, 300ish
            importlib.reload(settings)
            self.level.run(dt)
            pygame.mouse.set_visible(False)
            pygame.display.update()

if __name__ == '__main__':
    game = Game () 
    game.run()