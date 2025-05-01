"""
Mine module containing the Mine class.
"""
import pygame
from physics_engine.position import Position

class Mine:
    """Represents a mine that can damage spaceships."""
    
    def __init__(self, position: Position, cell_size: int):
        """Initialize the mine with position."""
        self.position = position
        self.cell_size = cell_size
        self.active = True
        # Load mine image
        self.image = pygame.image.load('assets/mine.png')
        # Scale image to cell size
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        
    def render(self, screen: pygame.Surface):
        """Render the mine if it's active"""
        if not self.active:
            return
            
        screen.blit(self.image, 
                   (self.position.x * self.cell_size, 
                    self.position.y * self.cell_size)) 