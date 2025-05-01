"""
Physics module for handling collision detection and movement validation.
"""
from typing import List, Tuple
from physics_engine.position import Position
from entities.laser import Laser
from entities.mine import Mine

class PhysicsEngine:
    def __init__(self, world_width: int, world_height: int, cell_size: int):
        self.world_width = world_width
        self.world_height = world_height
        self.cell_size = cell_size

    def check_wall_collision(self, position: Position, walls: List[Position]) -> bool:
        """Check if a position collides with any wall."""
        # Convert to grid coordinates
        grid_x = int(position.x)
        grid_y = int(position.y)
        return Position(grid_x, grid_y) in walls

    def check_mine_collision(self, position: Position, mine_position: Position) -> bool:
        """Check if a position collides with a mine."""
        # Convert to grid coordinates
        grid_x = int(position.x)
        grid_y = int(position.y)
        mine_grid_x = int(mine_position.x)
        mine_grid_y = int(mine_position.y)
        return grid_x == mine_grid_x and grid_y == mine_grid_y

    def check_laser_collision(self, laser_position: Position, target_position: Position) -> bool:
        """Check if a laser position collides with a target position."""
        # Convert to grid coordinates
        laser_grid_x = int(laser_position.x)
        laser_grid_y = int(laser_position.y)
        target_grid_x = int(target_position.x)
        target_grid_y = int(target_position.y)
        return laser_grid_x == target_grid_x and laser_grid_y == target_grid_y

    def is_valid_move(self, position: Position, walls: List[Position]) -> bool:
        """Check if a move to the given position is valid."""
        # Check wall collision
        if self.check_wall_collision(position, walls):
            return False
            
        # Check world boundaries (in grid coordinates)
        grid_width = self.world_width // self.cell_size
        grid_height = self.world_height // self.cell_size
        if (position.x < 0 or position.x >= grid_width or 
            position.y < 0 or position.y >= grid_height):
            return False
            
        return True

    def update_laser_position(self, laser: Laser, dt: float) -> bool:
        """Update laser position and check if it's still valid."""
        # Move laser
        laser.position.x += laser.direction.x * dt * laser.speed
        laser.position.y += laser.direction.y * dt * laser.speed
        
        # Check if laser is still in bounds (using grid coordinates)
        grid_width = self.world_width // self.cell_size
        grid_height = self.world_height // self.cell_size
        return (0 <= laser.position.x < grid_width and 
                0 <= laser.position.y < grid_height) 