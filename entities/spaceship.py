"""
Spaceship module containing the Spaceship class.
"""
import pygame
import math
import os
from typing import Tuple
from physics_engine.position import Position
from config.game_config import SHIELD_DURATION, INITIAL_LIFES

class Spaceship:
    """Represents a spaceship that can be rendered and controlled."""
    
    def __init__(self, cell_size: int = 30, name: str = None):
        """Initialize the spaceship with rendering properties."""
        self.cell_size = cell_size
        self.rotation = 0  # Rotation in degrees (0 = up, 90 = right, 180 = down, 270 = left)
        self.position = Position(1, 1)  # Initial position
        self.active = True
        self.lifes = INITIAL_LIFES
        self.id = None  # Will be set when player is registered
        self.name = name  # Player's display name
        
        # Shield state
        self.shield_active = False
        self.shield_available = True
        self.shield_start_time = 0
        self.shield_duration = SHIELD_DURATION

    def rotate(self, direction: str):
        """Rotate the spaceship by 90 degrees in the specified direction."""
        if direction == "right":
            self.rotation = (self.rotation + 90) % 360
        elif direction == "left":
            self.rotation = (self.rotation - 90) % 360

    def get_direction_vector(self) -> Position:
        """Get the movement direction vector based on current rotation."""
        angle_rad = math.radians(self.rotation)
        return Position(
            round(math.sin(angle_rad)),
            -round(math.cos(angle_rad))  # Negative because y increases downward
        )

    def render(self, screen: pygame.Surface):
        """Render the spaceship."""
        if not self.active:
            return
            
        self._load_image()  # Ensure image is loaded
            
        x = self.position.x * self.cell_size + self.cell_size // 2
        y = self.position.y * self.cell_size + self.cell_size // 2
        
        # Draw colored circle for player identification
        if self.id:
            color = self.colors.get(self.id, (255, 255, 255))  # Default to white if ID not found
            circle_radius = int(self.cell_size * 0.75)  # 0.75 blocks radius
            circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*color, 128), (circle_radius, circle_radius), circle_radius)  # 50% transparency
            screen.blit(circle_surface, (x - circle_radius, y - circle_radius))
        
        # Rotate and draw the spaceship image
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated_image.get_rect(center=(x, y))
        screen.blit(rotated_image, rect)

    def update_shield(self, current_time: float):
        """Update shield state."""
        if self.shield_active and current_time - self.shield_start_time >= self.shield_duration:
            self.shield_active = False 