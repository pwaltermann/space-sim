"""
Player statistics tracking module.
"""
from dataclasses import dataclass
from typing import Dict
import time
import csv
import os
from datetime import datetime

@dataclass
class PlayerStats:
    """Class to track player statistics."""
    start_time: float
    seconds_survived: float = 0
    laser_hits: int = 0
    lives_lost: int = 0
    is_last_surviving: bool = False
    
    def update_survival_time(self):
        """Update the survival time if the player is still active."""
        self.seconds_survived = time.time() - self.start_time
        
    def record_laser_hit(self):
        """Record a successful laser hit on another player."""
        self.laser_hits += 1
        
    def record_life_lost(self):
        """Record a life lost."""
        self.lives_lost += 1

class GameStats:
    """Class to manage game statistics and export."""
    
    def __init__(self):
        """Initialize game statistics."""
        self.player_stats: Dict[str, PlayerStats] = {}
        
    def add_player(self, player_id: str):
        """Add a new player to statistics tracking."""
        self.player_stats[player_id] = PlayerStats(start_time=time.time())
        
    def remove_player(self, player_id: str):
        """Remove a player from statistics tracking."""
        if player_id in self.player_stats:
            del self.player_stats[player_id]
            
    def update_stats(self, player_id: str, is_active: bool):
        """Update statistics for a player."""
        if player_id in self.player_stats:
            if is_active:
                self.player_stats[player_id].update_survival_time()
                
    def record_laser_hit(self, player_id: str):
        """Record a laser hit for a player."""
        if player_id in self.player_stats:
            self.player_stats[player_id].record_laser_hit()
            
    def record_life_lost(self, player_id: str):
        """Record a life lost for a player."""
        if player_id in self.player_stats:
            self.player_stats[player_id].record_life_lost()
            
    def set_last_surviving(self, player_id: str):
        """Mark a player as the last surviving player."""
        if player_id in self.player_stats:
            self.player_stats[player_id].is_last_surviving = True
            
    def export_stats(self):
        """Export game statistics to a CSV file."""
        # Create game_stats directory if it doesn't exist
        os.makedirs("game_stats", exist_ok=True)
        
        # Generate filename with current timestamp
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"game_stats/{timestamp}_gamestats.csv"
        
        # Write statistics to CSV file
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['player_id', 'seconds_survived', 'laser_hits', 'lives_lost', 'is_last_surviving']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for player_id, stats in self.player_stats.items():
                writer.writerow({
                    'player_id': player_id,
                    'seconds_survived': round(stats.seconds_survived, 2),
                    'laser_hits': stats.laser_hits,
                    'lives_lost': stats.lives_lost,
                    'is_last_surviving': stats.is_last_surviving
                }) 