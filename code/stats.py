import time

class StatUpdater:
    def __init__(self, player):
        self.player = player
        self.last_update_time = time.time()
        self.update_interval = 10  # Update every 10 seconds
        self.paused = False

    def update_stats_over_time(self):
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        
        # Decrease health and energy based on delta time
        health_decrease_amount = delta_time * 0.1  # Adjust this multiplier as needed
        energy_decrease_amount = delta_time * 0.4  # Adjust this multiplier as needed
        self.player.health -= health_decrease_amount
        self.player.energy -= energy_decrease_amount
        
        # Ensure health and energy don't go below zero
        self.player.health = max(0, self.player.health)
        self.player.energy = max(0, self.player.energy)

        # Update last update time
        self.last_update_time = current_time

    def update(self):
        if time.time() - self.last_update_time >= self.update_interval:
            self.update_stats_over_time()
            self.last_update_time = time.time()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def reset(self):
        self.player.energy = 100