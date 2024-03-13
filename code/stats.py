from settings import *
import time

class StatUpdater:
    def __init__(self, player):
        self.player = player
        self.last_update_time = time.time()
        self.update_interval = 3  # Update every 10 seconds
        self.active = True

    def update_stats_over_time(self):
        if self.active:
            current_time = time.time()
            delta_time = current_time - self.last_update_time
            
            health_decrease_amount = delta_time * 0.7  # speed of need decay
            energy_decrease_amount = delta_time * 6 
            self.player.health -= health_decrease_amount
            self.player.energy -= energy_decrease_amount
            
            # dont go below 0
            self.player.health = max(0, self.player.health)
            self.player.energy = max(0, self.player.energy)

            # sweepy self 
            if self.player.energy <= 30:
                self.player.speed = 100

            self.last_update_time = current_time

    def update(self):
        if time.time() - self.last_update_time >= self.update_interval:
            self.update_stats_over_time()
            self.last_update_time = time.time()

    def pause(self):
        self.active = False

    def resume(self):
        self.active = True

    def reset(self):
        self.player.energy = 100
        self.player.speed = SPEED