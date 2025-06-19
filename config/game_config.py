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


# wold 1

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



# world 2

OBSTACLE_WALLS2 = [
    (6, 3), (7, 3), (8, 3),
    (10, 4), (11, 5), (12, 6),
    (14, 4), (15, 4), (16, 4),

    (20, 3), (21, 3), (22, 4), (22, 5),
    (19, 6), (18, 7), (17, 8),

    (6, 9), (7, 9), (8, 10), (9, 11),
    (10, 12), (11, 12), (12, 12),

    (14, 10), (15, 10), (16, 10), (17, 10),
    (18, 11), (19, 12), (20, 13),

    (8, 15), (9, 15), (10, 15),
    (12, 16), (13, 17), (14, 17),

    (16, 16), (17, 15), (18, 15),
    (21, 14), (22, 13), (23, 12)
]


# map 3

OBSTACLE_WALLS3 = [
    (6, 2), (10, 2), (14, 2), (18, 2), (22, 2),
    (6, 3), (14, 3), (22, 3),
    (6, 4), (10, 4), (14, 4), (18, 4), (22, 4),

    (8, 6), (9, 6), (10, 6), (11, 6), (12, 6),
    (16, 6), (17, 6), (18, 6), (19, 6), (20, 6),

    (2, 8), (4, 8), (6, 8), (14, 8), (22, 8), (24, 8), (26, 8),
    (2, 9), (26, 9),
    (2, 10), (4, 10), (6, 10), (14, 10), (22, 10), (24, 10), (26, 10),

    (10, 12), (12, 12), (14, 12), (16, 12), (18, 12),
    (10, 13), (18, 13),
    (10, 14), (12, 14), (14, 14), (16, 14), (18, 14),

    (6, 16), (10, 16), (14, 16), (18, 16), (22, 16),
    (6, 17), (14, 17), (22, 17),
    (6, 18), (10, 18), (14, 18), (18, 18), (22, 18)
]

'''
# world 4, maybe try one world without walls
OBSTACLE_WALLS4 = [

]

'''




# Combine border and obstacle walls
WALLS: List[Tuple[int, int]] = BORDER_WALLS + OBSTACLE_WALLS2

'''
# Mine configuration with fixed positions
MINES: List[Tuple[int, int]] = [
    (8, 4), (13, 4),  # Upper mines
    (4, 12), (16, 12),  # Middle mines 
    (5, 17), (13, 15),  # Lower mines
    (19, 2), (24, 2), (12, 2),  # Additional upper row mines
]
'''
# mines 2

MINES = [
    # Upper section
    (2, 2), (13, 2), (18, 2), (25, 4),
    # Left corridor
    (3, 7), (5, 11), (4, 14),
    # Central areas
    (9, 7), (13, 8), (19, 9), (24, 10),
    # Right corridor
    (26, 7), (27, 11), (25, 15),
    # Lower section
    (11, 14), (15, 13), (20, 16)
]

'''
# Mines 3
MINES = [
    # Upper section
    (3, 2), (15, 2), (21, 3), (27, 2),
    # Middle-left section
    (5, 7), (7, 11), (3, 14),
    # Middle-center section
    (13, 9), (17, 12), (15, 15),
    # Middle-right section
    (23, 7), (25, 11), (27, 14),
    # Lower section
    (9, 17), (19, 16)
]
'''

# Player colors
PLAYER_COLORS = {
    "player1": RED,
    "player2": BLUE,
    "player3": GREEN,
    "player4": YELLOW
} 