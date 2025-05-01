"""
Laser module for handling laser behavior and properties.
"""
import pygame
from typing import Tuple
from physics_engine.position import Position
from config.game_config import CELL_SIZE, LASER_SPEED, LASER_LENGTH, RED

class Laser:
    """Represents a laser projectile in the game."""
    
    def __init__(self, position: Position, direction: Position, cell_size: int, owner_id: str):
        """
        Initialize a new laser.
        
        Args:
            position: Initial position of the laser
            direction: Direction vector of the laser
            cell_size: Size of a cell in pixels
            owner_id: ID of the entity that fired the laser
        """
        self.position = Position(position.x, position.y)
        self.direction = direction
        self.cell_size = cell_size
        self.owner_id = owner_id
        self.active = True
        self.speed = LASER_SPEED  # Using config value
        self.length = LASER_LENGTH  # Using config value
        
    def update(self, dt: float):
        """
        Update laser position based on direction and time.
        
        Args:
            dt: Time elapsed since last update
        """
        if not self.active:
            return
            
        # Move laser in its direction using configured speed
        self.position.x += self.direction.x * dt * self.speed
        self.position.y += self.direction.y * dt * self.speed
        
    def render(self, screen: pygame.Surface):
        """
        Render the laser on the screen.
        
        Args:
            screen: Pygame surface to render on
        """
        if not self.active:
            return
            
        # Draw laser as a red line
        start_pos = (
            int(self.position.x * self.cell_size + self.cell_size/2),
            int(self.position.y * self.cell_size + self.cell_size/2)
        )
        end_pos = (
            int((self.position.x + self.direction.x) * self.cell_size + self.cell_size/2),
            int((self.position.y + self.direction.y) * self.cell_size + self.cell_size/2)
        )
        pygame.draw.line(screen, RED, start_pos, end_pos, 2) 