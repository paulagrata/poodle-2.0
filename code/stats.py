from settings import *
import time

class StatUpdater:
    def __init__(self, player, clock):
        self.player = player
        self.clock = clock
        self.active = True
        self.last_decrease_time = None

    def update(self):
        hours, minutes, seconds = self.clock.calculate_time()
        if self.active:
            if minutes in (15, 45):
                if self.last_decrease_time is None or \
                        (hours != self.last_decrease_time[0] or minutes != self.last_decrease_time[1]):
                    self.player.health -= 5
                    self.player.energy -= 2
                    self.last_decrease_time = (hours, minutes)
            
            # dont go below 0
            self.player.health = max(0, self.player.health)
            self.player.energy = max(0, self.player.energy)

    def pause(self):
        self.active = False

    def resume(self):
        self.active = True

    def reset(self):
        self.player.energy = 100
        self.player.speed = SPEED