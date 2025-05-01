"""
Position module containing the Position class for 2D coordinates.
"""
from typing import Tuple

class Position:
    """Represents a 2D position in the game world."""
    
    def __init__(self, x: float, y: float):
        """Initialize position with x and y coordinates."""
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Check if two positions are equal."""
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Make Position hashable for use in sets and dictionaries."""
        return hash((self.x, self.y))

    def __add__(self, other: 'Position') -> 'Position':
        """Add two positions."""
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Position') -> 'Position':
        """Subtract two positions."""
        return Position(self.x - other.x, self.y - other.y)

    def to_tuple(self) -> Tuple[float, float]:
        """Convert position to tuple."""
        return (self.x, self.y) 