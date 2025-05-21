"""
Game configuration module containing all constants and game settings.
"""
from typing import List, Tuple

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
CELL_SIZE = 30

# Calculate grid dimensions based on screen size
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)


# Game settings
FPS = 60
SHIELD_DURATION = 3.0  # seconds
FLASH_DURATION = 0.5  # seconds
INITIAL_LIFES = 5

# Movement settings
LASER_SPEED = 10.0  # blocks per second
LASER_LENGTH = 0.5

# UI and rendering settings
PLAYER_CIRCLE_RADIUS_FACTOR = 0.75  # Player circle radius as fraction of cell size
SHIELD_RADIUS_FACTOR = 1.5  # Shield radius as fraction of cell size
UI_CIRCLE_RADIUS = 10  # Radius of player identifier circles in UI
TRANSPARENCY_ALPHA = 128  # Alpha value for semi-transparent elements (0-255)

# Wall configuration
# Generate border walls automatically based on screen dimensions
BORDER_WALLS = (
    [(x, 1) for x in range(GRID_WIDTH)] +  # Top wall
    [(x, GRID_HEIGHT - 1) for x in range(GRID_WIDTH)] +  # Bottom wall
    [(0, y) for y in range(GRID_HEIGHT)] +  # Left wall
    [(GRID_WIDTH-1, y) for y in range(GRID_HEIGHT)]   # Right wall
)

# Define the obstacle walls with fixed positions
OBSTACLE_WALLS = [
    # Inner walls near borders
    (10, 2), (20, 2),  # Near top border
    (10, 18), (20, 18),  # Near bottom border
    (10, 1), (10, 19),  # Near left border 
    (20, 1), (20, 19),  # Near right border
    # Upper region obstacles
    (8, 3), (22, 3),
    (6, 5), (24, 5), 
    (10, 4), (20, 4),
    
    # Middle region obstacles
    (7, 9), (23, 9),
    (9, 8), (21, 8),
    (8, 10), (22, 10),
    
    # Lower region obstacles
    (6, 15), (24, 15),
    (9, 16), (21, 16),
    (7, 17), (23, 17),
    
    # Scattered obstacles
    (5, 7), (25, 7),
    (8, 12), (22, 12),
    (10, 11), (20, 11),
    (7, 6), (23, 6),
    
    # Additional obstacles for larger grid
    (13, 7), (17, 7),
    (15, 9), (15, 13),
    (12, 14), (18, 14),
    (14, 8), (16, 8)
]

# Combine border and obstacle walls
WALLS: List[Tuple[int, int]] = BORDER_WALLS + OBSTACLE_WALLS

# Mine configuration with fixed positions
MINES: List[Tuple[int, int]] = [
    (8, 4), (13, 4),  # Upper mines
    (4, 12), (16, 12),  # Middle mines 
    (5, 17), (13, 15),  # Lower mines
    (19, 2), (24, 2), (12, 2),  # Additional upper row mines
]

# Player colors
PLAYER_COLORS = {
    "player1": RED,
    "player2": BLUE,
    "player3": GREEN,
    "player4": YELLOW
} 